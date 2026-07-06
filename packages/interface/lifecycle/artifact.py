from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .boundary import InterfaceBoundaryDescriptor, validate_interface_boundary_descriptor
from .states import (
    InterfaceLifecycleMetadata,
    InterfaceLifecycleState,
    validate_interface_lifecycle_metadata,
    validate_interface_lifecycle_state,
)


class InterfaceArtifactLifecycle(CanonicalObject):
    """Lifecycle record for interface artifacts at the constitutional boundary.

    Interface lifecycle states are descriptive architectural metadata. They SHALL NOT
    imply execution order, scheduling semantics, runtime progression, workflow
    orchestration, or automatic state transitions.

    Artifact references remain opaque identifiers whose interpretation belongs to other
    approved foundations or future authorized layers. Mission Charlie does not resolve
    references or perform lookup.

    Contract invariants:
    - Required fields: interface_lifecycle_state, boundary_descriptor, lifecycle_metadata, artifact_reference
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all lifecycle-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        interface_lifecycle_state: InterfaceLifecycleState,
        boundary_descriptor: InterfaceBoundaryDescriptor,
        artifact_reference: str,
        lifecycle_metadata: InterfaceLifecycleMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._interface_lifecycle_state = interface_lifecycle_state
        self._boundary_descriptor = boundary_descriptor
        self._artifact_reference = artifact_reference
        self._lifecycle_metadata = lifecycle_metadata or InterfaceLifecycleMetadata()
        self.register_validation_hook(validate_interface_artifact_lifecycle)

    @property
    def interface_lifecycle_state(self) -> InterfaceLifecycleState:
        return self._interface_lifecycle_state

    @property
    def boundary_descriptor(self) -> InterfaceBoundaryDescriptor:
        return self._boundary_descriptor

    @property
    def artifact_reference(self) -> str:
        return self._artifact_reference

    @property
    def lifecycle_metadata(self) -> InterfaceLifecycleMetadata:
        return self._lifecycle_metadata

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
            "interface_lifecycle_state": self.interface_lifecycle_state.value,
            "boundary_descriptor": self.boundary_descriptor.to_dict(),
            "artifact_reference": self.artifact_reference,
            "lifecycle_metadata": self.lifecycle_metadata.to_dict(),
        }


def validate_interface_artifact_lifecycle(obj: InterfaceArtifactLifecycle) -> ValidationResult:
    result = ValidationResult()

    interface_lifecycle_state = getattr(obj, "interface_lifecycle_state", None)
    if not isinstance(interface_lifecycle_state, InterfaceLifecycleState):
        result.add_error(
            "Lifecycle state must be an InterfaceLifecycleState value.",
            ValidationCategory.LIFECYCLE,
            field="interface_lifecycle_state",
            code="invalid_lifecycle_state",
        )
    else:
        result.merge(validate_interface_lifecycle_state(interface_lifecycle_state))

    boundary_descriptor = getattr(obj, "boundary_descriptor", None)
    if not isinstance(boundary_descriptor, InterfaceBoundaryDescriptor):
        result.add_error(
            "Boundary descriptor must be an InterfaceBoundaryDescriptor value.",
            ValidationCategory.SCHEMA,
            field="boundary_descriptor",
            code="invalid_boundary_descriptor",
        )
    else:
        result.merge(validate_interface_boundary_descriptor(boundary_descriptor))

    artifact_reference = getattr(obj, "artifact_reference", None)
    if not isinstance(artifact_reference, str) or not artifact_reference:
        result.add_error(
            "Artifact reference must be a non-empty opaque string.",
            ValidationCategory.IDENTITY,
            field="artifact_reference",
            code="invalid_artifact_reference",
        )

    lifecycle_metadata = getattr(obj, "lifecycle_metadata", None)
    if not isinstance(lifecycle_metadata, InterfaceLifecycleMetadata):
        result.add_error(
            "Lifecycle metadata must be an InterfaceLifecycleMetadata value.",
            ValidationCategory.METADATA,
            field="lifecycle_metadata",
            code="invalid_lifecycle_metadata",
        )
    else:
        result.merge(validate_interface_lifecycle_metadata(lifecycle_metadata))

    return result
