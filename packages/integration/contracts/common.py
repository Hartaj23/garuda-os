from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


@dataclass(frozen=True, slots=True)
class IntegrationContractMetadata:
    values: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.values, dict):
            object.__setattr__(self, "values", tuple(sorted(self.values.items())))
        elif isinstance(self.values, tuple):
            object.__setattr__(self, "values", tuple(sorted(self.values)))
        else:
            raise ValueError("values must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


@dataclass(frozen=True, slots=True)
class IntegrationParticipantReference:
    """Technology-neutral integration participant reference."""

    participant_identifier: str
    participant_metadata: IntegrationContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.participant_metadata is None:
            object.__setattr__(self, "participant_metadata", IntegrationContractMetadata())

    def to_dict(self) -> dict[str, object]:
        participant_metadata = self.participant_metadata or IntegrationContractMetadata()
        return {
            "participant_identifier": self.participant_identifier,
            "participant_metadata": participant_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class IntegrationParticipantReferenceCollection:
    references: tuple[IntegrationParticipantReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
        }


def validate_integration_contract_metadata(
    metadata: object,
    field_prefix: str = "contract_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, IntegrationContractMetadata):
        result.add_error(
            "Contract metadata must be an IntegrationContractMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_contract_metadata",
        )
        return result

    if not isinstance(metadata.values, tuple):
        result.add_error(
            "Contract metadata values must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.values",
            code="invalid_contract_metadata_values",
        )

    return result


def validate_integration_participant_reference(
    reference: object,
    field_prefix: str = "participant_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, IntegrationParticipantReference):
        result.add_error(
            "Participant reference must be an IntegrationParticipantReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_participant_reference",
        )
        return result

    if not isinstance(reference.participant_identifier, str) or not reference.participant_identifier:
        result.add_error(
            "Participant identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.participant_identifier",
            code="invalid_participant_identifier",
        )

    participant_metadata = reference.participant_metadata
    if participant_metadata is not None:
        result.merge(
            validate_integration_contract_metadata(
                participant_metadata,
                field_prefix=f"{field_prefix}.participant_metadata",
            )
        )

    return result


def validate_integration_participant_reference_collection(
    collection: object,
    field_prefix: str = "participant_references",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, IntegrationParticipantReferenceCollection):
        result.add_error(
            "Participant references must be an IntegrationParticipantReferenceCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_participant_reference_collection",
        )
        return result

    if not isinstance(collection.references, tuple):
        result.add_error(
            "Participant references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.references",
            code="invalid_participant_reference_collection_references",
        )
        return result

    for index, reference in enumerate(collection.references):
        result.merge(
            validate_integration_participant_reference(
                reference,
                field_prefix=f"{field_prefix}.references[{index}]",
            )
        )

    return result
