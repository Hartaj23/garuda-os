from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .boundary import IntegrationBoundaryDescriptor, validate_integration_boundary_descriptor
from .states import (
    IntegrationLifecycleMetadata,
    IntegrationLifecycleState,
    validate_integration_lifecycle_metadata,
    validate_integration_lifecycle_state,
)


class IntegrationArtifactLifecycle(CanonicalObject):
    """Lifecycle record for integration artifacts at the integration boundary layer.

    Integration lifecycle states are descriptive architectural metadata. They SHALL NOT imply
    execution order, scheduling semantics, runtime progression, workflow orchestration, or
    automatic state transitions.

    Artifact references remain opaque identifiers whose interpretation belongs to other approved
    foundations or future authorized layers. Mission Charlie does not resolve references or perform
    lookup.

    Contract invariants:
    - Required fields: integration_lifecycle_state, boundary_descriptor, lifecycle_metadata, artifact_reference
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all lifecycle-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        integration_lifecycle_state: IntegrationLifecycleState,
        boundary_descriptor: IntegrationBoundaryDescriptor,
        artifact_reference: str,
        lifecycle_metadata: IntegrationLifecycleMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._integration_lifecycle_state = integration_lifecycle_state
        self._boundary_descriptor = boundary_descriptor
        self._artifact_reference = artifact_reference
        self._lifecycle_metadata = lifecycle_metadata or IntegrationLifecycleMetadata()
        self.register_validation_hook(validate_integration_artifact_lifecycle)

    @property
    def integration_lifecycle_state(self) -> IntegrationLifecycleState:
        return self._integration_lifecycle_state

    @property
    def boundary_descriptor(self) -> IntegrationBoundaryDescriptor:
        return self._boundary_descriptor

    @property
    def artifact_reference(self) -> str:
        return self._artifact_reference

    @property
    def lifecycle_metadata(self) -> IntegrationLifecycleMetadata:
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
            "integration_lifecycle_state": self.integration_lifecycle_state.value,
            "boundary_descriptor": self.boundary_descriptor.to_dict(),
            "artifact_reference": self.artifact_reference,
            "lifecycle_metadata": self.lifecycle_metadata.to_dict(),
        }


def validate_integration_artifact_lifecycle(obj: IntegrationArtifactLifecycle) -> ValidationResult:
    result = ValidationResult()

    integration_lifecycle_state = getattr(obj, "integration_lifecycle_state", None)
    if not isinstance(integration_lifecycle_state, IntegrationLifecycleState):
        result.add_error(
            "Lifecycle state must be an IntegrationLifecycleState value.",
            ValidationCategory.LIFECYCLE,
            field="integration_lifecycle_state",
            code="invalid_lifecycle_state",
        )
    else:
        result.merge(validate_integration_lifecycle_state(integration_lifecycle_state))

    boundary_descriptor = getattr(obj, "boundary_descriptor", None)
    if not isinstance(boundary_descriptor, IntegrationBoundaryDescriptor):
        result.add_error(
            "Boundary descriptor must be an IntegrationBoundaryDescriptor value.",
            ValidationCategory.SCHEMA,
            field="boundary_descriptor",
            code="invalid_boundary_descriptor",
        )
    else:
        result.merge(validate_integration_boundary_descriptor(boundary_descriptor))

    artifact_reference = getattr(obj, "artifact_reference", None)
    if not isinstance(artifact_reference, str) or not artifact_reference:
        result.add_error(
            "Artifact reference must be a non-empty opaque string.",
            ValidationCategory.IDENTITY,
            field="artifact_reference",
            code="invalid_artifact_reference",
        )

    lifecycle_metadata = getattr(obj, "lifecycle_metadata", None)
    if not isinstance(lifecycle_metadata, IntegrationLifecycleMetadata):
        result.add_error(
            "Lifecycle metadata must be an IntegrationLifecycleMetadata value.",
            ValidationCategory.METADATA,
            field="lifecycle_metadata",
            code="invalid_lifecycle_metadata",
        )
    else:
        result.merge(validate_integration_lifecycle_metadata(lifecycle_metadata))

    return result
