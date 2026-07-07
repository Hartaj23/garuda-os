from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .metadata import IntegrationRegistryMetadata, validate_integration_registry_metadata


@dataclass(frozen=True, slots=True)
class IntegrationParticipantCatalogDeclaration:
    """Descriptive participant catalog classification for Integration Foundation metadata only.

    Catalog declarations classify integration participant metadata only. They do not imply
    execution permissions, scheduling authority, activation priority, or operational state.
    """

    catalog_identifier: str
    catalog_metadata: IntegrationRegistryMetadata | None = None

    def __post_init__(self) -> None:
        if self.catalog_metadata is None:
            object.__setattr__(self, "catalog_metadata", IntegrationRegistryMetadata())

    def to_dict(self) -> dict[str, object]:
        catalog_metadata = self.catalog_metadata or IntegrationRegistryMetadata()
        return {
            "catalog_identifier": self.catalog_identifier,
            "catalog_metadata": catalog_metadata.to_dict(),
        }


def validate_integration_participant_catalog_declaration(
    declaration: object,
    field_prefix: str = "catalog_declaration",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(declaration, IntegrationParticipantCatalogDeclaration):
        result.add_error(
            "Catalog declaration must be an IntegrationParticipantCatalogDeclaration value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_catalog_declaration",
        )
        return result

    if not isinstance(declaration.catalog_identifier, str) or not declaration.catalog_identifier:
        result.add_error(
            "Catalog identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.catalog_identifier",
            code="invalid_catalog_identifier",
        )

    catalog_metadata = declaration.catalog_metadata
    if catalog_metadata is not None:
        result.merge(
            validate_integration_registry_metadata(
                catalog_metadata,
                field_prefix=f"{field_prefix}.catalog_metadata",
            )
        )

    return result
