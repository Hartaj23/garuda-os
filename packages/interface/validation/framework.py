from __future__ import annotations

from typing import Any

from packages.interface.translation.representation import ExternalRepresentation
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .composition import compose_interface_validation_results
from .descriptor import (
    InterfaceValidationDescriptor,
    TARGET_OBJECT_TYPES,
    validate_interface_validation_descriptor,
)
from .metadata import InterfaceValidationMetadata, validate_interface_validation_metadata
from .policy import (
    InterfaceValidationPolicy,
    validate_artifact_version_compatibility,
    validate_interface_validation_policy,
)
from .result import InterfaceValidationOutcome, validation_result_to_outcome


CANONICAL_INTERFACE_ARTIFACT_TYPES = frozenset(TARGET_OBJECT_TYPES.values())


def evaluate_interface_artifact(
    artifact: object,
    policy: InterfaceValidationPolicy,
) -> ValidationResult:
    """Pure deterministic evaluation of a canonical interface artifact.

    Validation Containment Invariant:
    Only canonical Interface Foundation artifacts may enter the Validation Framework.

    evaluate_interface_artifact derives its result solely from the supplied canonical
    artifact and validation policy. It has no side effects, hidden state, environmental
    dependencies, or external lookups.
    """
    if isinstance(artifact, ExternalRepresentation):
        result = ValidationResult()
        result.add_error(
            "External representations are not eligible for interface validation.",
            ValidationCategory.SCHEMA,
            field="artifact",
            code="validation_containment_violation",
        )
        return result

    if not isinstance(artifact, CanonicalObject):
        result = ValidationResult()
        result.add_error(
            "Validation requires a canonical Interface Foundation artifact.",
            ValidationCategory.SCHEMA,
            field="artifact",
            code="invalid_validation_artifact",
        )
        return result

    if artifact.object_type not in CANONICAL_INTERFACE_ARTIFACT_TYPES:
        result = ValidationResult()
        result.add_error(
            "Artifact type is not an approved canonical Interface Foundation artifact.",
            ValidationCategory.SCHEMA,
            field="artifact.object_type",
            code="invalid_validation_artifact_type",
        )
        return result

    policy_result = validate_interface_validation_policy(policy)
    if policy.target_object_type != artifact.object_type:
        policy_result.add_error(
            "Validation policy target does not match artifact object type.",
            ValidationCategory.SCHEMA,
            field="artifact.object_type",
            code="policy_target_mismatch",
        )

    version_rule = policy.version_rule
    version_result = ValidationResult()
    if version_rule is not None:
        version_result = validate_artifact_version_compatibility(artifact, version_rule)

    artifact_result = artifact.validate()

    return compose_interface_validation_results(
        policy_result,
        version_result,
        artifact_result,
    )


class InterfaceValidationRecord(CanonicalObject):
    """Record of a canonical validation evaluation."""

    def __init__(
        self,
        validation_descriptor: InterfaceValidationDescriptor,
        validation_policy: InterfaceValidationPolicy,
        validation_outcome: InterfaceValidationOutcome,
        validation_metadata: InterfaceValidationMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._validation_descriptor = validation_descriptor
        self._validation_policy = validation_policy
        self._validation_outcome = validation_outcome
        self._validation_metadata = validation_metadata or InterfaceValidationMetadata()
        self.register_validation_hook(validate_interface_validation_record)

    @property
    def validation_descriptor(self) -> InterfaceValidationDescriptor:
        return self._validation_descriptor

    @property
    def validation_policy(self) -> InterfaceValidationPolicy:
        return self._validation_policy

    @property
    def validation_outcome(self) -> InterfaceValidationOutcome:
        return self._validation_outcome

    @property
    def validation_metadata(self) -> InterfaceValidationMetadata:
        return self._validation_metadata

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
            "validation_descriptor": self.validation_descriptor.to_dict(),
            "validation_policy": self.validation_policy.to_dict(),
            "validation_outcome": self.validation_outcome.to_dict(),
            "validation_metadata": self.validation_metadata.to_dict(),
        }


def validate_interface_validation_record(obj: InterfaceValidationRecord) -> ValidationResult:
    result = ValidationResult()

    validation_descriptor = getattr(obj, "validation_descriptor", None)
    if not isinstance(validation_descriptor, InterfaceValidationDescriptor):
        result.add_error(
            "Validation descriptor must be an InterfaceValidationDescriptor value.",
            ValidationCategory.SCHEMA,
            field="validation_descriptor",
            code="invalid_validation_descriptor",
        )
    else:
        result.merge(validate_interface_validation_descriptor(validation_descriptor))

    validation_policy = getattr(obj, "validation_policy", None)
    if not isinstance(validation_policy, InterfaceValidationPolicy):
        result.add_error(
            "Validation policy must be an InterfaceValidationPolicy value.",
            ValidationCategory.SCHEMA,
            field="validation_policy",
            code="invalid_validation_policy",
        )
    else:
        result.merge(validate_interface_validation_policy(validation_policy))

    validation_outcome = getattr(obj, "validation_outcome", None)
    if not isinstance(validation_outcome, InterfaceValidationOutcome):
        result.add_error(
            "Validation outcome must be an InterfaceValidationOutcome value.",
            ValidationCategory.SCHEMA,
            field="validation_outcome",
            code="invalid_validation_outcome",
        )

    validation_metadata = getattr(obj, "validation_metadata", None)
    if not isinstance(validation_metadata, InterfaceValidationMetadata):
        result.add_error(
            "Validation metadata must be an InterfaceValidationMetadata value.",
            ValidationCategory.METADATA,
            field="validation_metadata",
            code="invalid_validation_metadata",
        )
    else:
        result.merge(validate_interface_validation_metadata(validation_metadata))

    return result


__all__ = [
    "CANONICAL_INTERFACE_ARTIFACT_TYPES",
    "InterfaceValidationRecord",
    "evaluate_interface_artifact",
    "validate_interface_validation_record",
    "validation_result_to_outcome",
]
