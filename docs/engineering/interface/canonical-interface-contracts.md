# Canonical Interface Contracts

## Implementation Summary

GAR-SPRINT-0010 Mission Bravo adds canonical request and response contracts under
`packages/interface/contracts/`.

The implementation is intentionally limited:

- no production package outside `packages/interface` is modified
- no Platform Core behavior is changed
- no translation, registry, lifecycle, or validation framework behavior is introduced
- no transport, provider, runtime, or integration logic is introduced

## Public Interface

Import canonical contracts from `packages.interface`.

```python
from packages.interface import (
    CanonicalInterfacePayload,
    CanonicalInterfaceRequest,
    CanonicalInterfaceResponse,
    InterfaceContextReference,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
    InterfaceResponseStatus,
)
```

## Payload Neutrality

Use `CanonicalInterfacePayload` for technology-neutral canonical data only. Do not encode HTTP,
REST, gRPC, MCP, provider identifiers, or execution environment assumptions in payload values.

## Context References

Store opaque context identifiers through `InterfaceContextReference`. Do not resolve references
or import cognitive foundation packages from contract modules.

## Error Semantics

`InterfaceResponseWarning` and `InterfaceResponseError` define structure only:

- warning/ error message
- optional metadata container

Mission Bravo does not define error taxonomy, error codes, retry behavior, or recovery semantics.

## Deterministic Payloads

Use `CanonicalInterfaceRequest.to_dict()` and `CanonicalInterfaceResponse.to_dict()` for full
deterministic contract payloads. Use Platform Core `ObjectSerializer` only for inherited Platform
Core fields.

## Engineering Boundaries

Do not add translation, registry, lifecycle, validation framework rules, SDK examples, transport
protocols, providers, runtime behavior, or integration logic in Mission Bravo.

Do not modify Platform Core or any Phase I cognitive foundation package.

## Related Documents

- [Canonical Interface Contracts Architecture Guide](../../architecture/interface/canonical-interface-contracts.md)
- [Interface Foundation Overview](../../architecture/interface/overview.md)
