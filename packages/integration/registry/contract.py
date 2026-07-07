from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .descriptor import IntegrationParticipantDescriptor, validate_integration_participant_descriptor
from .metadata import IntegrationRegistryMetadata, validate_integration_registry_metadata


class IntegrationRegistrationContract(CanonicalObject):
    """Canonical registration contract for Integration Registry catalog entries.

    Registry Containment Invariant:
    The Integration Registry terminates registry knowledge within the Integration Foundation.
    Registry contents do not expose external technology representations, provider implementations,
    or internal cognitive implementation details.

    Contract invariants:
    - Required fields: registration_identifier, participant_descriptor, registration_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all registration-specific fields
    - Identity semantics: registration_identifier is the stable canonical catalog identity
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        registration_identifier: str,
        participant_descriptor: IntegrationParticipantDescriptor,
        registration_metadata: IntegrationRegistryMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._registration_identifier = registration_identifier
        self._participant_descriptor = participant_descriptor
        self._registration_metadata = registration_metadata or IntegrationRegistryMetadata()
        self.register_validation_hook(validate_integration_registration_contract)

    @property
    def registration_identifier(self) -> str:
        return self._registration_identifier

    @property
    def participant_descriptor(self) -> IntegrationParticipantDescriptor:
        return self._participant_descriptor

    @property
    def registration_metadata(self) -> IntegrationRegistryMetadata:
        return self._registration_metadata

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
            "registration_identifier": self.registration_identifier,
            "participant_descriptor": self.participant_descriptor.to_dict(),
            "registration_metadata": self.registration_metadata.to_dict(),
        }


def validate_integration_registration_contract(
    obj: IntegrationRegistrationContract,
) -> ValidationResult:
    result = ValidationResult()

    if (
        not isinstance(getattr(obj, "registration_identifier", None), str)
        or not obj.registration_identifier
    ):
        result.add_error(
            "Registration identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="registration_identifier",
            code="invalid_registration_identifier",
        )

    participant_descriptor = getattr(obj, "participant_descriptor", None)
    if not isinstance(participant_descriptor, IntegrationParticipantDescriptor):
        result.add_error(
            "Participant descriptor must be an IntegrationParticipantDescriptor value.",
            ValidationCategory.SCHEMA,
            field="participant_descriptor",
            code="invalid_participant_descriptor",
        )
    else:
        result.merge(validate_integration_participant_descriptor(participant_descriptor))

    registration_metadata = getattr(obj, "registration_metadata", None)
    if not isinstance(registration_metadata, IntegrationRegistryMetadata):
        result.add_error(
            "Registration metadata must be an IntegrationRegistryMetadata value.",
            ValidationCategory.METADATA,
            field="registration_metadata",
            code="invalid_registration_metadata",
        )
    else:
        result.merge(validate_integration_registry_metadata(registration_metadata))

    return result
