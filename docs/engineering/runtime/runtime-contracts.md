# Runtime Contracts

## Implementation Summary

GAR-SPRINT-0012 Mission Bravo adds runtime contract models under `packages/runtime/contracts/`.

The implementation is intentionally limited:

- no production package outside `packages/runtime` is modified
- no Integration Foundation contract modules are modified
- no Interface Foundation contract modules are modified
- no Platform Core behavior is changed
- no lifecycle, classification, validation framework, or registry behavior is introduced
- no transport, provider, Operational Runtime, or execution engine logic is introduced

## Public Interface

Import runtime contracts from `packages.runtime`.

```python
from packages.integration import CanonicalIntegrationContract
from packages.interface import CanonicalInterfaceRequest
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeContractMetadata,
    RuntimeContextReference,
    RuntimeContextReferenceCollection,
    build_integration_subordination,
    build_interface_subordination,
)
```

## Dual Subordination

Use builder helpers to link a runtime contract to predecessor contracts without modifying Integration
or Interface Foundation artifacts. Subordination helpers record structural identity relationships
only.

```python
interface_request = CanonicalInterfaceRequest(...)
integration_contract = CanonicalIntegrationContract(
    ...,
    interface_subordination=build_interface_subordination(interface_request),
    ...,
)
runtime_contract = CanonicalRuntimeContract(
    contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
    integration_subordination=build_integration_subordination(integration_contract),
    interface_subordination=build_interface_subordination(interface_request),
    context_references=RuntimeContextReferenceCollection(),
)

assert runtime_contract.integration_subordination.is_subordinate_to(integration_contract)
assert runtime_contract.interface_subordination.is_subordinate_to(interface_request)
```

## Runtime Context References

Store technology-neutral runtime context identifiers through `RuntimeContextReference`. Do not
encode credentials, transport protocols, execution engine bindings, or provider-specific identity
fields.

## Deterministic Payloads

Use `CanonicalRuntimeContract.to_dict()` for full deterministic contract payloads. Use Platform Core
`ObjectSerializer` only for inherited Platform Core fields.

## Engineering Boundaries

Do not add lifecycle, classification, validation framework rules, registry behavior, SDK examples,
transport protocols, providers, Operational Runtime behavior, or execution engines in Mission Bravo.

Do not modify Platform Core, Interface Foundation, Integration Foundation, or any Phase I cognitive
foundation package.

Do not embed policy or behavioral logic in subordination helpers.

## Related Documents

- [Runtime Contracts Architecture Guide](../../architecture/runtime/runtime-contracts.md)
- [Runtime Foundation Overview](../../architecture/runtime/overview.md)
