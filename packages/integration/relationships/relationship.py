from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .classification import (
    IntegrationParticipantClassificationHook,
    validate_integration_participant_classification_hook,
)
from .descriptor import (
    IntegrationParticipantRelationshipDescriptor,
    validate_integration_participant_relationship_descriptor,
)
from .metadata import IntegrationRelationshipMetadata, validate_integration_relationship_metadata


class CanonicalIntegrationRelationship(CanonicalObject):
    """Canonical integration relationship record for descriptive participant semantics.

    Relationship evaluation is descriptive architectural metadata. It SHALL NOT imply message
    routing, delivery, orchestration, scheduling, or operational execution.

    Contract invariants:
    - Required fields: relationship_descriptor, relationship_metadata, classification_hooks
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all relationship-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        relationship_descriptor: IntegrationParticipantRelationshipDescriptor,
        classification_hooks: tuple[IntegrationParticipantClassificationHook, ...] = (),
        relationship_metadata: IntegrationRelationshipMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._relationship_descriptor = relationship_descriptor
        self._classification_hooks = tuple(classification_hooks)
        self._relationship_metadata = relationship_metadata or IntegrationRelationshipMetadata()
        self.register_validation_hook(validate_canonical_integration_relationship)

    @property
    def relationship_descriptor(self) -> IntegrationParticipantRelationshipDescriptor:
        return self._relationship_descriptor

    @property
    def classification_hooks(self) -> tuple[IntegrationParticipantClassificationHook, ...]:
        return self._classification_hooks

    @property
    def relationship_metadata(self) -> IntegrationRelationshipMetadata:
        return self._relationship_metadata

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
            "relationship_descriptor": self.relationship_descriptor.to_dict(),
            "classification_hooks": [hook.to_dict() for hook in self.classification_hooks],
            "relationship_metadata": self.relationship_metadata.to_dict(),
        }


def validate_canonical_integration_relationship(obj: CanonicalIntegrationRelationship) -> ValidationResult:
    result = ValidationResult()

    relationship_descriptor = getattr(obj, "relationship_descriptor", None)
    if not isinstance(relationship_descriptor, IntegrationParticipantRelationshipDescriptor):
        result.add_error(
            "Relationship descriptor must be an IntegrationParticipantRelationshipDescriptor value.",
            ValidationCategory.SCHEMA,
            field="relationship_descriptor",
            code="invalid_relationship_descriptor",
        )
    else:
        result.merge(validate_integration_participant_relationship_descriptor(relationship_descriptor))

    classification_hooks = getattr(obj, "classification_hooks", None)
    if not isinstance(classification_hooks, tuple):
        result.add_error(
            "Classification hooks must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="classification_hooks",
            code="invalid_classification_hooks",
        )
    else:
        for index, hook in enumerate(classification_hooks):
            result.merge(
                validate_integration_participant_classification_hook(
                    hook,
                    field_prefix=f"classification_hooks[{index}]",
                )
            )

    relationship_metadata = getattr(obj, "relationship_metadata", None)
    if not isinstance(relationship_metadata, IntegrationRelationshipMetadata):
        result.add_error(
            "Relationship metadata must be an IntegrationRelationshipMetadata value.",
            ValidationCategory.METADATA,
            field="relationship_metadata",
            code="invalid_relationship_metadata",
        )
    else:
        result.merge(validate_integration_relationship_metadata(relationship_metadata))

    return result
