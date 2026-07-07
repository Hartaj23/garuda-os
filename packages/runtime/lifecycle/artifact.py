from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .boundary import RuntimeBoundaryDescriptor, validate_runtime_boundary_descriptor
from .states import (
    RuntimeLifecycleMetadata,
    RuntimeLifecycleState,
    validate_runtime_lifecycle_metadata,
    validate_runtime_lifecycle_state,
)


class RuntimeArtifactLifecycle(CanonicalObject):
    """Lifecycle record for runtime artifacts at the runtime boundary layer.

    Runtime lifecycle states are descriptive architectural metadata. They SHALL NOT imply
    execution order, scheduling semantics, operational runtime progression, workflow orchestration,
    or automatic state transitions.

    Artifact references remain opaque identifiers whose interpretation belongs to other approved
    foundations or future authorized layers. Mission Charlie does not resolve references or perform
    lookup.

    Contract invariants:
    - Required fields: runtime_lifecycle_state, boundary_descriptor, lifecycle_metadata, artifact_reference
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all lifecycle-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        runtime_lifecycle_state: RuntimeLifecycleState,
        boundary_descriptor: RuntimeBoundaryDescriptor,
        artifact_reference: str,
        lifecycle_metadata: RuntimeLifecycleMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._runtime_lifecycle_state = runtime_lifecycle_state
        self._boundary_descriptor = boundary_descriptor
        self._artifact_reference = artifact_reference
        self._lifecycle_metadata = lifecycle_metadata or RuntimeLifecycleMetadata()
        self.register_validation_hook(validate_runtime_artifact_lifecycle)

    @property
    def runtime_lifecycle_state(self) -> RuntimeLifecycleState:
        return self._runtime_lifecycle_state

    @property
    def boundary_descriptor(self) -> RuntimeBoundaryDescriptor:
        return self._boundary_descriptor

    @property
    def artifact_reference(self) -> str:
        return self._artifact_reference

    @property
    def lifecycle_metadata(self) -> RuntimeLifecycleMetadata:
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
            "runtime_lifecycle_state": self.runtime_lifecycle_state.value,
            "boundary_descriptor": self.boundary_descriptor.to_dict(),
            "artifact_reference": self.artifact_reference,
            "lifecycle_metadata": self.lifecycle_metadata.to_dict(),
        }


def validate_runtime_artifact_lifecycle(obj: RuntimeArtifactLifecycle) -> ValidationResult:
    result = ValidationResult()

    runtime_lifecycle_state = getattr(obj, "runtime_lifecycle_state", None)
    if not isinstance(runtime_lifecycle_state, RuntimeLifecycleState):
        result.add_error(
            "Lifecycle state must be a RuntimeLifecycleState value.",
            ValidationCategory.LIFECYCLE,
            field="runtime_lifecycle_state",
            code="invalid_lifecycle_state",
        )
    else:
        result.merge(validate_runtime_lifecycle_state(runtime_lifecycle_state, "runtime_lifecycle_state"))

    boundary_descriptor = getattr(obj, "boundary_descriptor", None)
    if not isinstance(boundary_descriptor, RuntimeBoundaryDescriptor):
        result.add_error(
            "Boundary descriptor must be a RuntimeBoundaryDescriptor value.",
            ValidationCategory.SCHEMA,
            field="boundary_descriptor",
            code="invalid_boundary_descriptor",
        )
    else:
        result.merge(validate_runtime_boundary_descriptor(boundary_descriptor))

    artifact_reference = getattr(obj, "artifact_reference", None)
    if not isinstance(artifact_reference, str) or not artifact_reference:
        result.add_error(
            "Artifact reference must be a non-empty opaque string.",
            ValidationCategory.IDENTITY,
            field="artifact_reference",
            code="invalid_artifact_reference",
        )

    lifecycle_metadata = getattr(obj, "lifecycle_metadata", None)
    if not isinstance(lifecycle_metadata, RuntimeLifecycleMetadata):
        result.add_error(
            "Lifecycle metadata must be a RuntimeLifecycleMetadata value.",
            ValidationCategory.METADATA,
            field="lifecycle_metadata",
            code="invalid_lifecycle_metadata",
        )
    else:
        result.merge(validate_runtime_lifecycle_metadata(lifecycle_metadata))

    return result
