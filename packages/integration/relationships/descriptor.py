from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.integration.contracts import IntegrationParticipantReference
from packages.objects import ValidationCategory, ValidationResult

from .metadata import IntegrationRelationshipMetadata, validate_integration_relationship_metadata


class IntegrationRelationshipKind(StrEnum):
    ASSOCIATED = "associated"
    DEPENDENT = "dependent"
    OBSERVES = "observes"
    AGGREGATES = "aggregates"


@dataclass(frozen=True, slots=True)
class IntegrationParticipantRelationshipDescriptor:
    """Descriptive relationship semantics between integration participants."""

    source_participant: IntegrationParticipantReference
    target_participant: IntegrationParticipantReference
    relationship_kind: IntegrationRelationshipKind
    relationship_metadata: IntegrationRelationshipMetadata | None = None

    def __post_init__(self) -> None:
        if self.relationship_metadata is None:
            object.__setattr__(self, "relationship_metadata", IntegrationRelationshipMetadata())

    def to_dict(self) -> dict[str, object]:
        relationship_metadata = self.relationship_metadata or IntegrationRelationshipMetadata()
        return {
            "source_participant": self.source_participant.to_dict(),
            "target_participant": self.target_participant.to_dict(),
            "relationship_kind": self.relationship_kind.value,
            "relationship_metadata": relationship_metadata.to_dict(),
        }


def validate_integration_participant_relationship_descriptor(
    descriptor: object,
    field_prefix: str = "relationship_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, IntegrationParticipantRelationshipDescriptor):
        result.add_error(
            "Relationship descriptor must be an IntegrationParticipantRelationshipDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_relationship_descriptor",
        )
        return result

    if not isinstance(descriptor.relationship_kind, IntegrationRelationshipKind):
        result.add_error(
            "Relationship kind must be an IntegrationRelationshipKind value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.relationship_kind",
            code="invalid_relationship_kind",
        )

    for role, participant in (
        ("source_participant", descriptor.source_participant),
        ("target_participant", descriptor.target_participant),
    ):
        if (
            not isinstance(participant.participant_identifier, str)
            or not participant.participant_identifier
        ):
            result.add_error(
                "Participant identifier must be a non-empty string.",
                ValidationCategory.IDENTITY,
                field=f"{field_prefix}.{role}.participant_identifier",
                code="invalid_participant_identifier",
            )

    relationship_metadata = descriptor.relationship_metadata
    if relationship_metadata is not None:
        result.merge(
            validate_integration_relationship_metadata(
                relationship_metadata,
                field_prefix=f"{field_prefix}.relationship_metadata",
            )
        )

    return result
