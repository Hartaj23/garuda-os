from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationResult

from .descriptor import (
    IntegrationParticipantRelationshipDescriptor,
    IntegrationRelationshipKind,
    validate_integration_participant_relationship_descriptor,
)
from .metadata import IntegrationRelationshipMetadata


@dataclass(frozen=True, slots=True)
class IntegrationRelationshipEvaluation:
    """Deterministic descriptive relationship evaluation result.

    Evaluation records architectural semantics only. It does not route messages, invoke providers,
    or perform operational integration execution.
    """

    relationship_kind: IntegrationRelationshipKind
    source_participant_identifier: str
    target_participant_identifier: str
    is_directional: bool
    evaluation_metadata: IntegrationRelationshipMetadata

    def to_dict(self) -> dict[str, object]:
        return {
            "relationship_kind": self.relationship_kind.value,
            "source_participant_identifier": self.source_participant_identifier,
            "target_participant_identifier": self.target_participant_identifier,
            "is_directional": self.is_directional,
            "evaluation_metadata": self.evaluation_metadata.to_dict(),
        }


_DIRECTIONAL_RELATIONSHIP_KINDS = frozenset(
    {
        IntegrationRelationshipKind.DEPENDENT,
        IntegrationRelationshipKind.OBSERVES,
    }
)


def evaluate_integration_relationship(
    descriptor: IntegrationParticipantRelationshipDescriptor,
) -> IntegrationRelationshipEvaluation:
    """Evaluate descriptive integration relationship semantics deterministically."""

    validation = validate_integration_participant_relationship_descriptor(descriptor)
    if not validation.is_valid:
        raise ValueError("Relationship descriptor failed validation before evaluation.")

    return IntegrationRelationshipEvaluation(
        relationship_kind=descriptor.relationship_kind,
        source_participant_identifier=descriptor.source_participant.participant_identifier,
        target_participant_identifier=descriptor.target_participant.participant_identifier,
        is_directional=descriptor.relationship_kind in _DIRECTIONAL_RELATIONSHIP_KINDS,
        evaluation_metadata=IntegrationRelationshipMetadata(
            values={
                "evaluation_scope": "descriptive",
                "relationship_kind": descriptor.relationship_kind.value,
            }
        ),
    )


def evaluate_integration_relationship_validation(
    descriptor: IntegrationParticipantRelationshipDescriptor,
) -> ValidationResult:
    return validate_integration_participant_relationship_descriptor(descriptor)
