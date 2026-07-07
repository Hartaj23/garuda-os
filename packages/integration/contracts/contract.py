from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import (
    IntegrationContractMetadata,
    IntegrationParticipantReferenceCollection,
    validate_integration_contract_metadata,
    validate_integration_participant_reference_collection,
)
from .subordination import (
    IntegrationContractSubordination,
    validate_integration_contract_subordination,
)


class CanonicalIntegrationContract(CanonicalObject):
    """Canonical integration contract subordinate to a canonical interface contract.

    Contract invariants:
    - Required fields: contract_metadata, interface_subordination, participant_references
    - Optional fields: Platform Core constructor fields (object_id, metadata, tags, lifecycle, audit)
    - Immutable after construction: all contract-specific fields
    - Equality semantics: not overridden; identity follows object identity semantics
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full contract via to_dict()
    - Subordination semantics: integration contract governance is subordinate to interface contracts
    """

    def __init__(
        self,
        contract_metadata: IntegrationContractMetadata,
        interface_subordination: IntegrationContractSubordination,
        participant_references: IntegrationParticipantReferenceCollection,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._contract_metadata = contract_metadata
        self._interface_subordination = interface_subordination
        self._participant_references = participant_references
        self.register_validation_hook(validate_canonical_integration_contract)

    @property
    def contract_metadata(self) -> IntegrationContractMetadata:
        return self._contract_metadata

    @property
    def interface_subordination(self) -> IntegrationContractSubordination:
        return self._interface_subordination

    @property
    def participant_references(self) -> IntegrationParticipantReferenceCollection:
        return self._participant_references

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
            "contract_metadata": self.contract_metadata.to_dict(),
            "interface_subordination": self.interface_subordination.to_dict(),
            "participant_references": self.participant_references.to_dict(),
        }


def validate_canonical_integration_contract(obj: CanonicalIntegrationContract) -> ValidationResult:
    result = ValidationResult()

    contract_metadata = getattr(obj, "contract_metadata", None)
    if not isinstance(contract_metadata, IntegrationContractMetadata):
        result.add_error(
            "Contract metadata must be an IntegrationContractMetadata value.",
            ValidationCategory.METADATA,
            field="contract_metadata",
            code="invalid_contract_metadata",
        )
    else:
        result.merge(validate_integration_contract_metadata(contract_metadata))

    interface_subordination = getattr(obj, "interface_subordination", None)
    if not isinstance(interface_subordination, IntegrationContractSubordination):
        result.add_error(
            "Interface subordination must be an IntegrationContractSubordination value.",
            ValidationCategory.METADATA,
            field="interface_subordination",
            code="invalid_interface_subordination",
        )
    else:
        result.merge(validate_integration_contract_subordination(interface_subordination))

    participant_references = getattr(obj, "participant_references", None)
    if not isinstance(participant_references, IntegrationParticipantReferenceCollection):
        result.add_error(
            "Participant references must be an IntegrationParticipantReferenceCollection value.",
            ValidationCategory.METADATA,
            field="participant_references",
            code="invalid_participant_references",
        )
    else:
        result.merge(validate_integration_participant_reference_collection(participant_references))

    return result
