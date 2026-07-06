# Interface Foundation SDK Best Practices

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## Use Interface Artifacts As Descriptive Records

Use Interface Foundation types to describe boundary communication, validation outcomes, and registry
entries. Do not use them as executors, service locators, provider bindings, or runtime orchestrators.

## Keep External Variability At The Boundary

Normalize external representations with `normalize_to_canonical_payload` before validation. Do not pass
`ExternalRepresentation` instances to `evaluate_interface_artifact`.

## Validate Before Sharing

Call `validate()` on `CanonicalObject` subclasses and use validation helpers for frozen value models
before passing payloads across package boundaries.

```python
from packages.interface import CanonicalInterfaceRequest, evaluate_interface_artifact

result = evaluate_interface_artifact(request, policy)
assert result.is_valid
```

## Use Deterministic Metadata Models

Use `InterfaceContractMetadata`, `InterfaceRegistryMetadata`, `TranslationMetadata`, and related frozen
dataclasses for small serializable maps. Dictionary inputs are sorted for stable `to_dict()` output.

## Treat Registry As Catalog Only

Use `InterfaceRegistry` to register and look up descriptive entries. Do not use it to instantiate,
activate, execute, or resolve registered artifacts.

## Preserve Dependency Direction

Interface Foundation depends on Platform Core. It may reference canonical artifact type strings but must
not import Phase I cognitive foundations in production modules.

## Use The Right Serialization Surface

Use artifact `to_dict()` for full deterministic payloads. Use Platform Core `ObjectSerializer.serialize()`
when only inherited object fields are required.

## Stay Inside Certified Boundaries

The certified SDK does not include runtime execution, provider integration, persistence, REST APIs,
orchestration, scheduling, outbound translation, or authentication as implemented behavior.
