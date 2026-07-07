from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.integration.contracts import IntegrationParticipantReference
from packages.objects import ValidationCategory, ValidationResult

from .metadata import IntegrationRelationshipMetadata, validate_integration_relationship_metadata


class IntegrationParticipantClassification(StrEnum):
    NEUTRAL = "neutral"
    SOURCE = "source"
    TARGET = "target"
    OBSERVER = "observer"
    ASSOCIATED = "associated"


@dataclass(frozen=True, slots=True)
class IntegrationParticipantClassificationHook:
    """Participant classification hook for descriptive integration taxonomy."""

    participant_reference: IntegrationParticipantReference
    classification: IntegrationParticipantClassification
    classification_metadata: IntegrationRelationshipMetadata | None = None

    def __post_init__(self) -> None:
        if self.classification_metadata is None:
            object.__setattr__(self, "classification_metadata", IntegrationRelationshipMetadata())

    def to_dict(self) -> dict[str, object]:
        classification_metadata = self.classification_metadata or IntegrationRelationshipMetadata()
        return {
            "participant_reference": self.participant_reference.to_dict(),
            "classification": self.classification.value,
            "classification_metadata": classification_metadata.to_dict(),
        }


def validate_integration_participant_classification_hook(
    hook: object,
    field_prefix: str = "classification_hook",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(hook, IntegrationParticipantClassificationHook):
        result.add_error(
            "Classification hook must be an IntegrationParticipantClassificationHook value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_hook",
        )
        return result

    if not isinstance(hook.classification, IntegrationParticipantClassification):
        result.add_error(
            "Classification must be an IntegrationParticipantClassification value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.classification",
            code="invalid_classification",
        )

    if (
        not isinstance(hook.participant_reference.participant_identifier, str)
        or not hook.participant_reference.participant_identifier
    ):
        result.add_error(
            "Participant reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.participant_reference.participant_identifier",
            code="invalid_participant_reference_identifier",
        )

    classification_metadata = hook.classification_metadata
    if classification_metadata is not None:
        result.merge(
            validate_integration_relationship_metadata(
                classification_metadata,
                field_prefix=f"{field_prefix}.classification_metadata",
            )
        )

    return result
