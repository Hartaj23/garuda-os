# Integration Registry

## Purpose

Architecture documentation for the deterministic Integration Registry introduced by
GAR-SPRINT-0011 Mission Foxtrot.

## Registry Purity

Registry operations describe registered Integration Foundation artifacts only. They have no side
effects beyond deterministic catalog maintenance and do not instantiate, activate, execute, or
resolve registered artifacts.

## Lookup Neutrality

Registry lookups return descriptive registration information only. Lookup results do not expose
implementation instances, runtime handles, provider bindings, or transport-specific artifacts.

## Registration Identity

Registry entries are uniquely identifiable through immutable canonical `registration_identifier`
values. Registration rejects duplicate canonical identities deterministically.

## Participant Catalog Classification

Registry catalog declarations classify integration participant metadata only. They do not imply
execution permissions, scheduling authority, activation priority, or operational state.

## Registry Containment Invariant

The Integration Registry terminates registry knowledge within the Integration Foundation. Registry
contents do not expose external technology representations, provider implementations, or internal
cognitive implementation details.

## Registry Composition

Registry participant descriptors must align with published Integration Foundation artifact types.
Composition validation ensures registry entries remain descriptive and subordinate to the published
integration artifact model.

## Catalog vs Container

The registry records what exists. It does not determine what runs.

## Explicit Exclusions

Mission Foxtrot does not implement service location, dependency injection, plugin discovery,
runtime registration, provider registration, persistence, operational integration, or Phase I
modifications.

## Related Documents

- [Integration Registry Engineering Guide](../../engineering/integration/integration-registry.md)
- [Integration Foundation Architecture Diagram](integration-foundation-architecture-diagram.md)
