from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .states import IntegrationLifecycleMetadata, validate_integration_lifecycle_metadata


class IntegrationBoundarySide(StrEnum):
    EXTERNAL = "external"
    MEMBRANE_TRAVERSAL = "membrane_traversal"


@dataclass(frozen=True, slots=True)
class IntegrationBoundaryExclusivity:
    """Declares that integration architecture traverses the constitutional membrane."""

    traverses_membrane: bool = True
    exclusivity_metadata: IntegrationLifecycleMetadata | None = None

    def __post_init__(self) -> None:
        if self.exclusivity_metadata is None:
            object.__setattr__(self, "exclusivity_metadata", IntegrationLifecycleMetadata())

    def to_dict(self) -> dict[str, object]:
        exclusivity_metadata = self.exclusivity_metadata or IntegrationLifecycleMetadata()
        return {
            "traverses_membrane": self.traverses_membrane,
            "exclusivity_metadata": exclusivity_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class IntegrationBoundaryDescriptor:
    boundary_identifier: str
    boundary_side: IntegrationBoundarySide
    exclusivity: IntegrationBoundaryExclusivity
    boundary_metadata: IntegrationLifecycleMetadata | None = None

    def __post_init__(self) -> None:
        if self.boundary_metadata is None:
            object.__setattr__(self, "boundary_metadata", IntegrationLifecycleMetadata())

    def to_dict(self) -> dict[str, object]:
        boundary_metadata = self.boundary_metadata or IntegrationLifecycleMetadata()
        return {
            "boundary_identifier": self.boundary_identifier,
            "boundary_side": self.boundary_side.value,
            "exclusivity": self.exclusivity.to_dict(),
            "boundary_metadata": boundary_metadata.to_dict(),
        }


class IntegrationBoundaryModel(CanonicalObject):
    """Integration boundary model enforcing membrane traversal through the Interface Foundation.

    The IntegrationBoundaryModel describes integration boundary relationships and invariants.
    It does not perform routing, dispatch, transport, authorization, connectivity, or execution.

    Architectural invariant:
    Integration architecture SHALL traverse the constitutional membrane exclusively through the
    Interface Foundation.

    Contract invariants:
    - Required fields: boundary_identifier, boundary_side, exclusivity, boundary_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all boundary-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full model via to_dict()
    """

    def __init__(
        self,
        boundary_identifier: str,
        boundary_side: IntegrationBoundarySide,
        exclusivity: IntegrationBoundaryExclusivity | None = None,
        boundary_metadata: IntegrationLifecycleMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._boundary_identifier = boundary_identifier
        self._boundary_side = boundary_side
        self._exclusivity = exclusivity or IntegrationBoundaryExclusivity()
        self._boundary_metadata = boundary_metadata or IntegrationLifecycleMetadata()
        self.register_validation_hook(validate_integration_boundary_model)

    @property
    def boundary_identifier(self) -> str:
        return self._boundary_identifier

    @property
    def boundary_side(self) -> IntegrationBoundarySide:
        return self._boundary_side

    @property
    def exclusivity(self) -> IntegrationBoundaryExclusivity:
        return self._exclusivity

    @property
    def boundary_metadata(self) -> IntegrationLifecycleMetadata:
        return self._boundary_metadata

    def to_descriptor(self) -> IntegrationBoundaryDescriptor:
        return IntegrationBoundaryDescriptor(
            boundary_identifier=self.boundary_identifier,
            boundary_side=self.boundary_side,
            exclusivity=self.exclusivity,
            boundary_metadata=self.boundary_metadata,
        )

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
            "boundary_identifier": self.boundary_identifier,
            "boundary_side": self.boundary_side.value,
            "exclusivity": self.exclusivity.to_dict(),
            "boundary_metadata": self.boundary_metadata.to_dict(),
        }


def validate_integration_boundary_exclusivity(
    exclusivity: object,
    field_prefix: str = "exclusivity",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(exclusivity, IntegrationBoundaryExclusivity):
        result.add_error(
            "Boundary exclusivity must be an IntegrationBoundaryExclusivity value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_boundary_exclusivity",
        )
        return result

    if exclusivity.traverses_membrane is not True:
        result.add_error(
            "Integration architecture must traverse the constitutional membrane.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.traverses_membrane",
            code="invalid_boundary_exclusivity_assertion",
        )

    exclusivity_metadata = exclusivity.exclusivity_metadata
    if exclusivity_metadata is not None:
        result.merge(
            validate_integration_lifecycle_metadata(
                exclusivity_metadata,
                field_prefix=f"{field_prefix}.exclusivity_metadata",
            )
        )

    return result


def validate_integration_boundary_descriptor(
    descriptor: object,
    field_prefix: str = "boundary_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, IntegrationBoundaryDescriptor):
        result.add_error(
            "Boundary descriptor must be an IntegrationBoundaryDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_boundary_descriptor",
        )
        return result

    if not isinstance(descriptor.boundary_identifier, str) or not descriptor.boundary_identifier:
        result.add_error(
            "Boundary identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.boundary_identifier",
            code="invalid_boundary_identifier",
        )

    if not isinstance(descriptor.boundary_side, IntegrationBoundarySide):
        result.add_error(
            "Boundary side must be an IntegrationBoundarySide value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.boundary_side",
            code="invalid_boundary_side",
        )

    result.merge(
        validate_integration_boundary_exclusivity(
            descriptor.exclusivity,
            field_prefix=f"{field_prefix}.exclusivity",
        )
    )

    boundary_metadata = descriptor.boundary_metadata
    if boundary_metadata is not None:
        result.merge(
            validate_integration_lifecycle_metadata(
                boundary_metadata,
                field_prefix=f"{field_prefix}.boundary_metadata",
            )
        )

    return result


def validate_integration_boundary_model(obj: IntegrationBoundaryModel) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "boundary_identifier", None), str) or not obj.boundary_identifier:
        result.add_error(
            "Boundary identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="boundary_identifier",
            code="invalid_boundary_identifier",
        )

    if not isinstance(getattr(obj, "boundary_side", None), IntegrationBoundarySide):
        result.add_error(
            "Boundary side must be an IntegrationBoundarySide value.",
            ValidationCategory.SCHEMA,
            field="boundary_side",
            code="invalid_boundary_side",
        )

    exclusivity = getattr(obj, "exclusivity", None)
    if not isinstance(exclusivity, IntegrationBoundaryExclusivity):
        result.add_error(
            "Boundary exclusivity must be an IntegrationBoundaryExclusivity value.",
            ValidationCategory.SCHEMA,
            field="exclusivity",
            code="invalid_boundary_exclusivity",
        )
    else:
        result.merge(validate_integration_boundary_exclusivity(exclusivity))

    boundary_metadata = getattr(obj, "boundary_metadata", None)
    if not isinstance(boundary_metadata, IntegrationLifecycleMetadata):
        result.add_error(
            "Boundary metadata must be an IntegrationLifecycleMetadata value.",
            ValidationCategory.METADATA,
            field="boundary_metadata",
            code="invalid_boundary_metadata",
        )
    else:
        result.merge(validate_integration_lifecycle_metadata(boundary_metadata))

    return result
