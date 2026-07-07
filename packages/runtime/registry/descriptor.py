from __future__ import annotations

from dataclasses import dataclass

from packages.runtime.validation import (
    CANONICAL_RUNTIME_ARTIFACT_TYPES,
    RuntimeVersionCompatibilityRule,
    validate_runtime_version_compatibility_rule,
)
from packages.objects import ValidationCategory, ValidationResult

from .catalog import RuntimeContextCatalogDeclaration, validate_runtime_context_catalog_declaration
from .metadata import RuntimeRegistryMetadata, validate_runtime_registry_metadata


@dataclass(frozen=True, slots=True)
class RuntimeContextDescriptor:
    """Descriptive runtime context descriptor — not a provider implementation."""

    context_identifier: str
    artifact_object_type: str
    catalog_declarations: tuple[RuntimeContextCatalogDeclaration, ...] = ()
    descriptor_metadata: RuntimeRegistryMetadata | None = None
    version_compatibility: RuntimeVersionCompatibilityRule | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "catalog_declarations", tuple(self.catalog_declarations))
        if self.descriptor_metadata is None:
            object.__setattr__(self, "descriptor_metadata", RuntimeRegistryMetadata())
        if self.version_compatibility is None:
            object.__setattr__(
                self,
                "version_compatibility",
                RuntimeVersionCompatibilityRule(),
            )

    def to_dict(self) -> dict[str, object]:
        descriptor_metadata = self.descriptor_metadata or RuntimeRegistryMetadata()
        version_compatibility = self.version_compatibility or RuntimeVersionCompatibilityRule()
        return {
            "context_identifier": self.context_identifier,
            "artifact_object_type": self.artifact_object_type,
            "catalog_declarations": [
                declaration.to_dict() for declaration in self.catalog_declarations
            ],
            "descriptor_metadata": descriptor_metadata.to_dict(),
            "version_compatibility": version_compatibility.to_dict(),
        }


def validate_runtime_context_descriptor(
    descriptor: object,
    field_prefix: str = "context_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, RuntimeContextDescriptor):
        result.add_error(
            "Context descriptor must be a RuntimeContextDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_context_descriptor",
        )
        return result

    if not isinstance(descriptor.context_identifier, str) or not descriptor.context_identifier:
        result.add_error(
            "Context identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.context_identifier",
            code="invalid_context_identifier",
        )

    if (
        not isinstance(descriptor.artifact_object_type, str)
        or descriptor.artifact_object_type not in CANONICAL_RUNTIME_ARTIFACT_TYPES
    ):
        result.add_error(
            "Artifact object type must be an approved canonical Runtime Foundation artifact type.",
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
                validate_runtime_context_catalog_declaration(
                    declaration,
                    field_prefix=f"{field_prefix}.catalog_declarations[{index}]",
                )
            )

    descriptor_metadata = descriptor.descriptor_metadata
    if descriptor_metadata is not None:
        result.merge(
            validate_runtime_registry_metadata(
                descriptor_metadata,
                field_prefix=f"{field_prefix}.descriptor_metadata",
            )
        )

    version_compatibility = descriptor.version_compatibility
    if version_compatibility is not None:
        result.merge(
            validate_runtime_version_compatibility_rule(
                version_compatibility,
                field_prefix=f"{field_prefix}.version_compatibility",
            )
        )

    return result
