from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import (
    RuntimeContractMetadata,
    RuntimeContextReferenceCollection,
    validate_runtime_contract_metadata,
    validate_runtime_context_reference_collection,
)
from .subordination import (
    RuntimeIntegrationContractSubordination,
    RuntimeInterfaceContractSubordination,
    validate_runtime_integration_contract_subordination,
    validate_runtime_interface_contract_subordination,
)


class CanonicalRuntimeContract(CanonicalObject):
    """Canonical runtime contract subordinate to integration and interface contracts.

    Contract invariants:
    - Required fields: contract_metadata, integration_subordination, interface_subordination,
      context_references
    - Optional fields: Platform Core constructor fields (object_id, metadata, tags, lifecycle, audit)
    - Immutable after construction: all contract-specific fields
    - Equality semantics: not overridden; identity follows object identity semantics
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full contract via to_dict()
    - Subordination semantics: runtime contract governance is subordinate to integration and interface
      contracts
    """

    def __init__(
        self,
        contract_metadata: RuntimeContractMetadata,
        integration_subordination: RuntimeIntegrationContractSubordination,
        interface_subordination: RuntimeInterfaceContractSubordination,
        context_references: RuntimeContextReferenceCollection,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._contract_metadata = contract_metadata
        self._integration_subordination = integration_subordination
        self._interface_subordination = interface_subordination
        self._context_references = context_references
        self.register_validation_hook(validate_canonical_runtime_contract)

    @property
    def contract_metadata(self) -> RuntimeContractMetadata:
        return self._contract_metadata

    @property
    def integration_subordination(self) -> RuntimeIntegrationContractSubordination:
        return self._integration_subordination

    @property
    def interface_subordination(self) -> RuntimeInterfaceContractSubordination:
        return self._interface_subordination

    @property
    def context_references(self) -> RuntimeContextReferenceCollection:
        return self._context_references

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
            "integration_subordination": self.integration_subordination.to_dict(),
            "interface_subordination": self.interface_subordination.to_dict(),
            "context_references": self.context_references.to_dict(),
        }


def validate_canonical_runtime_contract(obj: CanonicalRuntimeContract) -> ValidationResult:
    result = ValidationResult()

    contract_metadata = getattr(obj, "contract_metadata", None)
    if not isinstance(contract_metadata, RuntimeContractMetadata):
        result.add_error(
            "Contract metadata must be a RuntimeContractMetadata value.",
            ValidationCategory.METADATA,
            field="contract_metadata",
            code="invalid_contract_metadata",
        )
    else:
        result.merge(validate_runtime_contract_metadata(contract_metadata))

    integration_subordination = getattr(obj, "integration_subordination", None)
    if not isinstance(integration_subordination, RuntimeIntegrationContractSubordination):
        result.add_error(
            "Integration subordination must be a RuntimeIntegrationContractSubordination value.",
            ValidationCategory.METADATA,
            field="integration_subordination",
            code="invalid_integration_subordination",
        )
    else:
        result.merge(validate_runtime_integration_contract_subordination(integration_subordination))

    interface_subordination = getattr(obj, "interface_subordination", None)
    if not isinstance(interface_subordination, RuntimeInterfaceContractSubordination):
        result.add_error(
            "Interface subordination must be a RuntimeInterfaceContractSubordination value.",
            ValidationCategory.METADATA,
            field="interface_subordination",
            code="invalid_interface_subordination",
        )
    else:
        result.merge(validate_runtime_interface_contract_subordination(interface_subordination))

    context_references = getattr(obj, "context_references", None)
    if not isinstance(context_references, RuntimeContextReferenceCollection):
        result.add_error(
            "Context references must be a RuntimeContextReferenceCollection value.",
            ValidationCategory.METADATA,
            field="context_references",
            code="invalid_context_references",
        )
    else:
        result.merge(validate_runtime_context_reference_collection(context_references))

    return result
