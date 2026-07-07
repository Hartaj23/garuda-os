# Integration Contracts

## Purpose

Architecture documentation for integration contracts subordinate to canonical interface contracts,
introduced by GAR-SPRINT-0011 Mission Bravo.

## Contract Invariants

### CanonicalIntegrationContract

| Invariant | Definition |
| --- | --- |
| Required fields | `contract_metadata`, `interface_subordination`, `participant_references` |
| Optional fields | Platform Core constructor fields (`object_id`, metadata, tags, lifecycle, audit) |
| Immutable after construction | All contract-specific fields |
| Equality semantics | Not overridden; object identity semantics apply |
| Identity semantics | Platform Core `object_id` and `object_type` inherited unchanged |
| Serialization | Inherited Platform Core fields via `ObjectSerializer`; full contract via `to_dict()` |
| Subordination semantics | Integration contract governance is subordinate to canonical interface contracts |

### IntegrationContractSubordination

| Invariant | Definition |
| --- | --- |
| Required fields | `interface_contract_object_id`, `interface_contract_object_type` |
| Allowed interface types | `CanonicalInterfaceRequest`, `CanonicalInterfaceResponse` |
| Subordination rule | Integration contracts SHALL NOT supersede membrane communication semantics |

## Participant References

`IntegrationParticipantReference` stores technology-neutral participant identifiers only.
Mission Bravo SHALL NOT encode provider credentials, transport semantics, or operational connectivity.

## Object Model

`CanonicalIntegrationContract` inherits from Platform Core `CanonicalObject`. Shared contract
abstractions are immutable frozen value models.

## Explicit Exclusions

Mission Bravo does not implement lifecycle, relationship semantics, validation framework rules,
registry behavior, SDK guides, transport protocols, providers, runtime behavior, or operational
integration execution.

## Related Documents

- [Integration Foundation Overview](overview.md)
- [Integration Contracts Engineering Guide](../../engineering/integration/integration-contracts.md)
