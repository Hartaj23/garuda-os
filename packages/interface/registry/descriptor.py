from __future__ import annotations

from dataclasses import dataclass, field

from packages.interface.validation.policy import (
    InterfaceVersionCompatibilityRule,
    validate_interface_version_compatibility_rule,
)
from packages.objects import ValidationCategory, ValidationResult

from .capability import InterfaceCapabilityDeclaration, validate_interface_capability_declaration
from .metadata import InterfaceRegistryMetadata, validate_interface_registry_metadata


@dataclass(frozen=True, slots=True)
class InterfaceAdapterDescriptor:
    """Descriptive adapter descriptor — not a provider implementation."""

    adapter_identifier: str
    artifact_object_type: str
    capability_declarations: tuple[InterfaceCapabilityDeclaration, ...] = ()
    descriptor_metadata: InterfaceRegistryMetadata | None = None
    version_compatibility: InterfaceVersionCompatibilityRule | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "capability_declarations", tuple(self.capability_declarations))
        if self.descriptor_metadata is None:
            object.__setattr__(self, "descriptor_metadata", InterfaceRegistryMetadata())
        if self.version_compatibility is None:
            object.__setattr__(
                self,
                "version_compatibility",
                InterfaceVersionCompatibilityRule(),
            )

    def to_dict(self) -> dict[str, object]:
        descriptor_metadata = self.descriptor_metadata or InterfaceRegistryMetadata()
        version_compatibility = self.version_compatibility or InterfaceVersionCompatibilityRule()
        return {
            "adapter_identifier": self.adapter_identifier,
            "artifact_object_type": self.artifact_object_type,
            "capability_declarations": [
                capability.to_dict() for capability in self.capability_declarations
            ],
            "descriptor_metadata": descriptor_metadata.to_dict(),
            "version_compatibility": version_compatibility.to_dict(),
        }


def validate_interface_adapter_descriptor(
    descriptor: object,
    field_prefix: str = "adapter_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, InterfaceAdapterDescriptor):
        result.add_error(
            "Adapter descriptor must be an InterfaceAdapterDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_adapter_descriptor",
        )
        return result

    if not isinstance(descriptor.adapter_identifier, str) or not descriptor.adapter_identifier:
        result.add_error(
            "Adapter identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.adapter_identifier",
            code="invalid_adapter_identifier",
        )

    if not isinstance(descriptor.artifact_object_type, str) or not descriptor.artifact_object_type:
        result.add_error(
            "Artifact object type must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.artifact_object_type",
            code="invalid_artifact_object_type",
        )

    if not isinstance(descriptor.capability_declarations, tuple):
        result.add_error(
            "Capability declarations must be stored as an immutable tuple.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.capability_declarations",
            code="invalid_capability_declarations",
        )
    else:
        for index, capability in enumerate(descriptor.capability_declarations):
            result.merge(
                validate_interface_capability_declaration(
                    capability,
                    field_prefix=f"{field_prefix}.capability_declarations[{index}]",
                )
            )

    descriptor_metadata = descriptor.descriptor_metadata
    if descriptor_metadata is not None:
        result.merge(
            validate_interface_registry_metadata(
                descriptor_metadata,
                field_prefix=f"{field_prefix}.descriptor_metadata",
            )
        )

    version_compatibility = descriptor.version_compatibility
    if version_compatibility is not None:
        result.merge(
            validate_interface_version_compatibility_rule(
                version_compatibility,
                field_prefix=f"{field_prefix}.version_compatibility",
            )
        )

    return result
