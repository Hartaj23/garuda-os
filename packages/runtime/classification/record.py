from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult
from packages.runtime.contracts.common import RuntimeContextReference

from .metadata import RuntimeClassificationMetadata, validate_runtime_classification_metadata
from .taxonomy import (
    RuntimeContextClassification,
    RuntimeContextClassificationHookCollection,
    validate_runtime_context_classification_hook_collection,
)


class CanonicalRuntimeContextClassification(CanonicalObject):
    """Canonical runtime context classification record.

    Runtime context classifications are descriptive architectural metadata. They SHALL NOT imply
    routing, invocation, scheduling, operational runtime progression, or execution engine binding.

    Contract invariants:
    - Required fields: context_reference, classification, classification_hooks, classification_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all classification-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        context_reference: RuntimeContextReference,
        classification: RuntimeContextClassification,
        classification_hooks: RuntimeContextClassificationHookCollection | None = None,
        classification_metadata: RuntimeClassificationMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._context_reference = context_reference
        self._classification = classification
        self._classification_hooks = classification_hooks or RuntimeContextClassificationHookCollection()
        self._classification_metadata = classification_metadata or RuntimeClassificationMetadata()
        self.register_validation_hook(validate_canonical_runtime_context_classification)

    @property
    def context_reference(self) -> RuntimeContextReference:
        return self._context_reference

    @property
    def classification(self) -> RuntimeContextClassification:
        return self._classification

    @property
    def classification_hooks(self) -> RuntimeContextClassificationHookCollection:
        return self._classification_hooks

    @property
    def classification_metadata(self) -> RuntimeClassificationMetadata:
        return self._classification_metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "object_version": self.object_version,
            "object_type": self.object_type,
            "object_id": str(self.object_id),
            "metadata": dict(sorted(self.metadata.values.items())),
            "tags": list(self.tags),
            "lifecycle_state": self.lifecycle_state.value,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "context_reference": self.context_reference.to_dict(),
            "classification": self.classification.value,
            "classification_hooks": self.classification_hooks.to_dict(),
            "classification_metadata": self.classification_metadata.to_dict(),
        }


def validate_canonical_runtime_context_classification(
    obj: CanonicalRuntimeContextClassification,
) -> ValidationResult:
    result = ValidationResult()

    context_reference = getattr(obj, "context_reference", None)
    if not isinstance(context_reference, RuntimeContextReference):
        result.add_error(
            "Context reference must be a RuntimeContextReference value.",
            ValidationCategory.METADATA,
            field="context_reference",
            code="invalid_context_reference",
        )
    elif (
        not isinstance(context_reference.context_identifier, str)
        or not context_reference.context_identifier
    ):
        result.add_error(
            "Context reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="context_reference.context_identifier",
            code="invalid_context_reference_identifier",
        )

    classification = getattr(obj, "classification", None)
    if not isinstance(classification, RuntimeContextClassification):
        result.add_error(
            "Classification must be a RuntimeContextClassification value.",
            ValidationCategory.SCHEMA,
            field="classification",
            code="invalid_classification",
        )

    classification_hooks = getattr(obj, "classification_hooks", None)
    if not isinstance(classification_hooks, RuntimeContextClassificationHookCollection):
        result.add_error(
            "Classification hooks must be a RuntimeContextClassificationHookCollection value.",
            ValidationCategory.METADATA,
            field="classification_hooks",
            code="invalid_classification_hooks",
        )
    else:
        result.merge(validate_runtime_context_classification_hook_collection(classification_hooks))

    classification_metadata = getattr(obj, "classification_metadata", None)
    if not isinstance(classification_metadata, RuntimeClassificationMetadata):
        result.add_error(
            "Classification metadata must be a RuntimeClassificationMetadata value.",
            ValidationCategory.METADATA,
            field="classification_metadata",
            code="invalid_classification_metadata",
        )
    else:
        result.merge(validate_runtime_classification_metadata(classification_metadata))

    return result
