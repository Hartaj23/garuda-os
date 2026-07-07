from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .contract import IntegrationRegistrationContract, validate_integration_registration_contract
from .descriptor import IntegrationParticipantDescriptor


@dataclass(frozen=True, slots=True)
class IntegrationRegistryEntry:
    registration_identifier: str
    registration_contract: IntegrationRegistrationContract
    participant_descriptor: IntegrationParticipantDescriptor

    def __post_init__(self) -> None:
        if self.registration_identifier != self.registration_contract.registration_identifier:
            raise ValueError(
                "registration_identifier must match registration_contract.registration_identifier"
            )
        if self.participant_descriptor != self.registration_contract.participant_descriptor:
            raise ValueError(
                "participant_descriptor must match registration_contract.participant_descriptor"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "registration_contract": self.registration_contract.to_dict(),
            "participant_descriptor": self.participant_descriptor.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class IntegrationRegistryLookupCriteria:
    registration_identifier: str | None = None
    artifact_object_type: str | None = None
    participant_identifier: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "artifact_object_type": self.artifact_object_type,
            "participant_identifier": self.participant_identifier,
        }


@dataclass(frozen=True, slots=True)
class IntegrationRegistryLookupResult:
    entries: tuple[IntegrationRegistryEntry, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))

    def to_dict(self) -> dict[str, object]:
        return {
            "entries": [entry.to_dict() for entry in self.entries],
        }


def validate_integration_registry_entry(
    entry: object,
    field_prefix: str = "registry_entry",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(entry, IntegrationRegistryEntry):
        result.add_error(
            "Registry entry must be an IntegrationRegistryEntry value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_registry_entry",
        )
        return result

    if not isinstance(entry.registration_identifier, str) or not entry.registration_identifier:
        result.add_error(
            "Registration identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.registration_identifier",
            code="invalid_registration_identifier",
        )

    if not isinstance(entry.registration_contract, IntegrationRegistrationContract):
        result.add_error(
            "Registration contract must be an IntegrationRegistrationContract value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.registration_contract",
            code="invalid_registration_contract",
        )
    else:
        result.merge(validate_integration_registration_contract(entry.registration_contract))

    if not isinstance(entry.participant_descriptor, IntegrationParticipantDescriptor):
        result.add_error(
            "Participant descriptor must be an IntegrationParticipantDescriptor value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.participant_descriptor",
            code="invalid_participant_descriptor",
        )

    return result
