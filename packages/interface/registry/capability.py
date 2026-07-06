from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .metadata import InterfaceRegistryMetadata, validate_interface_registry_metadata


@dataclass(frozen=True, slots=True)
class InterfaceCapabilityDeclaration:
    """Descriptive capability classification for Interface Foundation functionality only.

    Capabilities classify Interface Foundation functionality only. They do not imply
    execution permissions, scheduling authority, activation priority, or operational state.
    """

    capability_identifier: str
    capability_metadata: InterfaceRegistryMetadata | None = None

    def __post_init__(self) -> None:
        if self.capability_metadata is None:
            object.__setattr__(self, "capability_metadata", InterfaceRegistryMetadata())

    def to_dict(self) -> dict[str, object]:
        capability_metadata = self.capability_metadata or InterfaceRegistryMetadata()
        return {
            "capability_identifier": self.capability_identifier,
            "capability_metadata": capability_metadata.to_dict(),
        }


def validate_interface_capability_declaration(
    capability: object,
    field_prefix: str = "capability_declaration",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(capability, InterfaceCapabilityDeclaration):
        result.add_error(
            "Capability declaration must be an InterfaceCapabilityDeclaration value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_capability_declaration",
        )
        return result

    if not isinstance(capability.capability_identifier, str) or not capability.capability_identifier:
        result.add_error(
            "Capability identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.capability_identifier",
            code="invalid_capability_identifier",
        )

    capability_metadata = capability.capability_metadata
    if capability_metadata is not None:
        result.merge(
            validate_interface_registry_metadata(
                capability_metadata,
                field_prefix=f"{field_prefix}.capability_metadata",
            )
        )

    return result
