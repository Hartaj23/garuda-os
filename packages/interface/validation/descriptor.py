from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.objects import ValidationCategory, ValidationResult

from .metadata import InterfaceValidationMetadata, validate_interface_validation_metadata


class InterfaceValidationTarget(StrEnum):
    FOUNDATION = "foundation"
    REQUEST = "request"
    RESPONSE = "response"
    TRANSLATION = "translation"
    BOUNDARY = "boundary"
    LIFECYCLE = "lifecycle"


TARGET_OBJECT_TYPES: dict[InterfaceValidationTarget, str] = {
    InterfaceValidationTarget.FOUNDATION: "InterfaceFoundation",
    InterfaceValidationTarget.REQUEST: "CanonicalInterfaceRequest",
    InterfaceValidationTarget.RESPONSE: "CanonicalInterfaceResponse",
    InterfaceValidationTarget.TRANSLATION: "CanonicalTranslationContract",
    InterfaceValidationTarget.BOUNDARY: "InterfaceBoundaryModel",
    InterfaceValidationTarget.LIFECYCLE: "InterfaceArtifactLifecycle",
}


@dataclass(frozen=True, slots=True)
class InterfaceValidationDescriptor:
    validation_target: InterfaceValidationTarget
    target_object_type: str
    descriptor_metadata: InterfaceValidationMetadata | None = None

    def __post_init__(self) -> None:
        if self.descriptor_metadata is None:
            object.__setattr__(self, "descriptor_metadata", InterfaceValidationMetadata())
        expected = TARGET_OBJECT_TYPES.get(self.validation_target)
        if expected is not None and self.target_object_type != expected:
            raise ValueError(
                "target_object_type must match the canonical object type for validation_target"
            )

    def to_dict(self) -> dict[str, object]:
        descriptor_metadata = self.descriptor_metadata or InterfaceValidationMetadata()
        return {
            "validation_target": self.validation_target.value,
            "target_object_type": self.target_object_type,
            "descriptor_metadata": descriptor_metadata.to_dict(),
        }


def validate_interface_validation_descriptor(
    descriptor: object,
    field_prefix: str = "validation_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, InterfaceValidationDescriptor):
        result.add_error(
            "Validation descriptor must be an InterfaceValidationDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_validation_descriptor",
        )
        return result

    if not isinstance(descriptor.validation_target, InterfaceValidationTarget):
        result.add_error(
            "Validation target must be an InterfaceValidationTarget value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.validation_target",
            code="invalid_validation_target",
        )

    if not isinstance(descriptor.target_object_type, str) or not descriptor.target_object_type:
        result.add_error(
            "Target object type must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.target_object_type",
            code="invalid_target_object_type",
        )

    descriptor_metadata = descriptor.descriptor_metadata
    if descriptor_metadata is not None:
        result.merge(
            validate_interface_validation_metadata(
                descriptor_metadata,
                field_prefix=f"{field_prefix}.descriptor_metadata",
            )
        )

    return result
