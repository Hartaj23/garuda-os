# Integration Contracts

## Implementation Summary

GAR-SPRINT-0011 Mission Bravo adds integration contract models under `packages/integration/contracts/`.

The implementation is intentionally limited:

- no production package outside `packages/integration` is modified
- no Interface Foundation contract modules are modified
- no Platform Core behavior is changed
- no lifecycle, relationship, validation framework, or registry behavior is introduced
- no transport, provider, runtime, or operational integration logic is introduced

## Public Interface

Import integration contracts from `packages.integration`.

```python
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationContractSubordination,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    build_interface_subordination,
)
from packages.interface import CanonicalInterfaceRequest
```

## Subordination

Use `build_interface_subordination()` to link an integration contract to a canonical interface
contract without modifying Interface Foundation artifacts.

```python
interface_request = CanonicalInterfaceRequest(...)
integration_contract = CanonicalIntegrationContract(
    contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
    interface_subordination=build_interface_subordination(interface_request),
    participant_references=IntegrationParticipantReferenceCollection(),
)

assert integration_contract.interface_subordination.is_subordinate_to(interface_request)
```

## Participant References

Store technology-neutral participant identifiers through `IntegrationParticipantReference`.
Do not encode credentials, transport protocols, or provider-specific identity fields.

## Deterministic Payloads

Use `CanonicalIntegrationContract.to_dict()` for full deterministic contract payloads. Use Platform
Core `ObjectSerializer` only for inherited Platform Core fields.

## Engineering Boundaries

Do not add lifecycle, relationship semantics, validation framework rules, registry behavior, SDK
examples, transport protocols, providers, runtime behavior, or operational integration execution in
Mission Bravo.

Do not modify Platform Core, Interface Foundation, or any Phase I cognitive foundation package.

## Related Documents

- [Integration Contracts Architecture Guide](../../architecture/integration/integration-contracts.md)
- [Integration Foundation Overview](../../architecture/integration/overview.md)
