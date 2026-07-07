from __future__ import annotations

from dataclasses import dataclass

from packages.integration.validation import (
    CANONICAL_INTEGRATION_ARTIFACT_TYPES,
    IntegrationVersionCompatibilityRule,
    validate_integration_version_compatibility_rule,
)
from packages.objects import ValidationCategory, ValidationResult

from .catalog import (
    IntegrationParticipantCatalogDeclaration,
    validate_integration_participant_catalog_declaration,
)
from .metadata import IntegrationRegistryMetadata, validate_integration_registry_metadata


@dataclass(frozen=True, slots=True)
class IntegrationParticipantDescriptor:
    """Descriptive participant descriptor — not a provider implementation."""

    participant_identifier: str
    artifact_object_type: str
    catalog_declarations: tuple[IntegrationParticipantCatalogDeclaration, ...] = ()
    descriptor_metadata: IntegrationRegistryMetadata | None = None
    version_compatibility: IntegrationVersionCompatibilityRule | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "catalog_declarations", tuple(self.catalog_declarations))
        if self.descriptor_metadata is None:
            object.__setattr__(self, "descriptor_metadata", IntegrationRegistryMetadata())
        if self.version_compatibility is None:
            object.__setattr__(
                self,
                "version_compatibility",
                IntegrationVersionCompatibilityRule(),
            )

    def to_dict(self) -> dict[str, object]:
        descriptor_metadata = self.descriptor_metadata or IntegrationRegistryMetadata()
        version_compatibility = self.version_compatibility or IntegrationVersionCompatibilityRule()
        return {
            "participant_identifier": self.participant_identifier,
            "artifact_object_type": self.artifact_object_type,
            "catalog_declarations": [
                declaration.to_dict() for declaration in self.catalog_declarations
            ],
            "descriptor_metadata": descriptor_metadata.to_dict(),
            "version_compatibility": version_compatibility.to_dict(),
        }


def validate_integration_participant_descriptor(
    descriptor: object,
    field_prefix: str = "participant_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, IntegrationParticipantDescriptor):
        result.add_error(
            "Participant descriptor must be an IntegrationParticipantDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_participant_descriptor",
        )
        return result

    if not isinstance(descriptor.participant_identifier, str) or not descriptor.participant_identifier:
        result.add_error(
            "Participant identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.participant_identifier",
            code="invalid_participant_identifier",
        )

    if (
        not isinstance(descriptor.artifact_object_type, str)
        or descriptor.artifact_object_type not in CANONICAL_INTEGRATION_ARTIFACT_TYPES
    ):
        result.add_error(
            "Artifact object type must be an approved canonical Integration Foundation artifact type.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.artifact_object_type",
            code="invalid_artifact_object_type",
        )

    if not isinstance(descriptor.catalog_declarations, tuple):
        result.add_error(
            "Catalog declarations must be stored as an immutable tuple.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.catalog_declarations",
            code="invalid_catalog_declarations",
        )
    else:
        for index, declaration in enumerate(descriptor.catalog_declarations):
            result.merge(
                validate_integration_participant_catalog_declaration(
                    declaration,
                    field_prefix=f"{field_prefix}.catalog_declarations[{index}]",
                )
            )

    descriptor_metadata = descriptor.descriptor_metadata
    if descriptor_metadata is not None:
        result.merge(
            validate_integration_registry_metadata(
                descriptor_metadata,
                field_prefix=f"{field_prefix}.descriptor_metadata",
            )
        )

    version_compatibility = descriptor.version_compatibility
    if version_compatibility is not None:
        result.merge(
            validate_integration_version_compatibility_rule(
                version_compatibility,
                field_prefix=f"{field_prefix}.version_compatibility",
            )
        )

    return result
