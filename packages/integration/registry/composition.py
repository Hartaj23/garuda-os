from __future__ import annotations

from packages.integration.validation import CANONICAL_INTEGRATION_ARTIFACT_TYPES
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .contract import IntegrationRegistrationContract, validate_integration_registration_contract
from .descriptor import IntegrationParticipantDescriptor, validate_integration_participant_descriptor
from .lookup import IntegrationRegistryEntry, validate_integration_registry_entry


def validate_integration_registry_artifact_composition(
    artifact: CanonicalObject,
    participant_descriptor: IntegrationParticipantDescriptor,
    field_prefix: str = "registry_composition",
) -> ValidationResult:
    """Verify registry participant descriptors align with published integration artifacts."""

    result = ValidationResult()

    if artifact.object_type not in CANONICAL_INTEGRATION_ARTIFACT_TYPES:
        result.add_error(
            "Artifact type is not an approved canonical Integration Foundation artifact.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.artifact.object_type",
            code="invalid_registry_artifact_type",
        )
        return result

    if participant_descriptor.artifact_object_type != artifact.object_type:
        result.add_error(
            "Participant descriptor artifact type must match the supplied integration artifact.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.participant_descriptor.artifact_object_type",
            code="registry_artifact_type_mismatch",
        )

    result.merge(validate_integration_participant_descriptor(participant_descriptor))

    return result


def compose_integration_registry_entry(
    registration_contract: IntegrationRegistrationContract,
) -> IntegrationRegistryEntry:
    """Compose a deterministic registry entry from a canonical registration contract."""

    validation = validate_integration_registration_contract(registration_contract)
    if not validation.is_valid:
        raise ValueError("Registration contract failed validation before composition.")

    entry = IntegrationRegistryEntry(
        registration_identifier=registration_contract.registration_identifier,
        registration_contract=registration_contract,
        participant_descriptor=registration_contract.participant_descriptor,
    )

    entry_validation = validate_integration_registry_entry(entry)
    if not entry_validation.is_valid:
        raise ValueError("Registry entry failed validation after composition.")

    return entry
