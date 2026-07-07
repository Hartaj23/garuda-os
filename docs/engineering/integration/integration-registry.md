# Integration Registry

## Implementation Summary

GAR-SPRINT-0011 Mission Foxtrot adds the deterministic Integration Registry catalog under
`packages/integration/registry/`.

The implementation is intentionally limited:

- process-local descriptive catalog only
- deterministic lookup semantics
- no instantiation, activation, execution, or resolution APIs

## Public Interface

```python
from packages.integration import (
    IntegrationParticipantDescriptor,
    IntegrationRegistrationContract,
    IntegrationRegistry,
    IntegrationRegistryEntry,
    IntegrationRegistryLookupCriteria,
    compose_integration_registry_entry,
)

entry = compose_integration_registry_entry(registration_contract)
registry = IntegrationRegistry()
registry.register(entry)
result = registry.lookup(
    IntegrationRegistryLookupCriteria(
        artifact_object_type="CanonicalIntegrationContract",
    )
)
```

## Registry Composition

Use `compose_integration_registry_entry()` to construct deterministic registry entries from
canonical registration contracts. Use `validate_integration_registry_artifact_composition()` to
verify participant descriptors align with published integration artifacts.

## Engineering Boundaries

Do not add service locator behavior, dependency injection, plugin discovery, dynamic loading,
runtime registration, provider registration, transport registration, execution routing, or
persistence.

Do not modify frozen Mission Alpha–Echo production modules except cumulative export wiring.

## Related Documents

- [Integration Registry Architecture Guide](../../architecture/integration/integration-registry.md)
- [Integration Foundation Architecture Diagram](../../architecture/integration/integration-foundation-architecture-diagram.md)
