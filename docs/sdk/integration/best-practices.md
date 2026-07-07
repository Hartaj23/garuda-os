# Integration Foundation SDK Best Practices

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Use Integration Artifacts As Descriptive Records

Use Integration Foundation types to describe participant metadata, contract governance, lifecycle
state, relationships, validation outcomes, and registry entries. Do not use them as executors,
service locators, provider bindings, or runtime orchestrators.

## Preserve Interface Subordination

Always link integration contracts to canonical interface contracts using
`build_interface_subordination()`. Do not invent standalone interface contract identifiers.

## Validate Before Sharing

Call `validate()` on `CanonicalObject` subclasses and use validation helpers for frozen value models
before passing payloads across package boundaries.

```python
from packages.integration import evaluate_integration_artifact, IntegrationValidationPolicy

result = evaluate_integration_artifact(contract, policy)
assert result.is_valid
```

## Use Deterministic Metadata Models

Use `IntegrationContractMetadata`, `IntegrationRegistryMetadata`, `IntegrationRelationshipMetadata`,
and related frozen dataclasses for small serializable maps. Dictionary inputs are sorted for stable
`to_dict()` output.

## Treat Registry As Catalog Only

Use `IntegrationRegistry` to register and look up descriptive entries. Do not use it to instantiate,
activate, execute, or resolve registered artifacts.

## Preserve Dependency Direction

Integration Foundation depends on Platform Core and lawfully consumes Interface Foundation. Do not
import Phase I cognitive foundations in Integration consumer code unless separately authorized.

## Use The Right Serialization Surface

Use artifact `to_dict()` for full deterministic payloads. Use Platform Core `ObjectSerializer.serialize()`
when only inherited object fields are required.

## Stay Inside Certified Boundaries

The certified SDK does not include runtime execution, provider integration, persistence, transport,
orchestration, scheduling, or authentication as implemented behavior.

See [Coding Conventions](coding-conventions.md) for detailed usage standards.
