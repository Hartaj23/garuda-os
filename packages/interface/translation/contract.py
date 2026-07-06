from __future__ import annotations

from typing import Any

from packages.interface.contracts.common import CanonicalInterfacePayload
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .descriptor import TranslationDescriptor, validate_translation_descriptor
from .metadata import TranslationMetadata, validate_translation_metadata
from .representation import ExternalRepresentation, validate_external_representation


class CanonicalTranslationContract(CanonicalObject):
    """Canonical translation contract for inbound architectural translation.

    Translation Containment Invariant:
    External representations terminate at the Translation Framework. Only canonical
    representations may exit the Translation Framework toward the Internal Cognitive
    Foundations.

    Contract invariants:
    - Required fields: translation_descriptor, source_representation, canonical_payload, translation_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all translation-specific fields
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full contract via to_dict()
    """

    def __init__(
        self,
        translation_descriptor: TranslationDescriptor,
        source_representation: ExternalRepresentation,
        canonical_payload: CanonicalInterfacePayload,
        translation_metadata: TranslationMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._translation_descriptor = translation_descriptor
        self._source_representation = source_representation
        self._canonical_payload = canonical_payload
        self._translation_metadata = translation_metadata or TranslationMetadata()
        self.register_validation_hook(validate_canonical_translation_contract)

    @property
    def translation_descriptor(self) -> TranslationDescriptor:
        return self._translation_descriptor

    @property
    def source_representation(self) -> ExternalRepresentation:
        return self._source_representation

    @property
    def canonical_payload(self) -> CanonicalInterfacePayload:
        return self._canonical_payload

    @property
    def translation_metadata(self) -> TranslationMetadata:
        return self._translation_metadata

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
            "translation_descriptor": self.translation_descriptor.to_dict(),
            "source_representation": self.source_representation.to_dict(),
            "canonical_payload": self.canonical_payload.to_dict(),
            "translation_metadata": self.translation_metadata.to_dict(),
        }


def validate_canonical_translation_contract(
    obj: CanonicalTranslationContract,
) -> ValidationResult:
    result = ValidationResult()

    translation_descriptor = getattr(obj, "translation_descriptor", None)
    if not isinstance(translation_descriptor, TranslationDescriptor):
        result.add_error(
            "Translation descriptor must be a TranslationDescriptor value.",
            ValidationCategory.SCHEMA,
            field="translation_descriptor",
            code="invalid_translation_descriptor",
        )
    else:
        result.merge(validate_translation_descriptor(translation_descriptor))

    source_representation = getattr(obj, "source_representation", None)
    if not isinstance(source_representation, ExternalRepresentation):
        result.add_error(
            "Source representation must be an ExternalRepresentation value.",
            ValidationCategory.SCHEMA,
            field="source_representation",
            code="invalid_source_representation",
        )
    else:
        result.merge(validate_external_representation(source_representation))

    canonical_payload = getattr(obj, "canonical_payload", None)
    if not isinstance(canonical_payload, CanonicalInterfacePayload):
        result.add_error(
            "Canonical payload must be a CanonicalInterfacePayload value.",
            ValidationCategory.SCHEMA,
            field="canonical_payload",
            code="invalid_canonical_payload",
        )

    translation_metadata = getattr(obj, "translation_metadata", None)
    if not isinstance(translation_metadata, TranslationMetadata):
        result.add_error(
            "Translation metadata must be a TranslationMetadata value.",
            ValidationCategory.METADATA,
            field="translation_metadata",
            code="invalid_translation_metadata",
        )
    else:
        result.merge(validate_translation_metadata(translation_metadata))

    return result
