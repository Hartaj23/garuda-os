# Runtime Foundation SDK Best Practices

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Use Runtime Artifacts As Descriptive Records

Use Runtime Foundation types to describe contract governance, lifecycle state, context
classification, validation outcomes, and registry entries. Do not use them as executors, service
locators, provider bindings, or operational runtime orchestrators.

## Preserve Dual Subordination

Always link runtime contracts to both canonical integration contracts and canonical interface
contracts using `build_integration_subordination()` and `build_interface_subordination()`. Do not
invent standalone contract identifiers that bypass predecessor foundations.

## Validate Before Sharing

Call `validate()` on `CanonicalObject` subclasses and use validation helpers for frozen value models
before passing payloads across package boundaries.

```python
from packages.runtime import evaluate_runtime_artifact, RuntimeValidationPolicy

result = evaluate_runtime_artifact(contract, policy)
assert result.is_valid
```

## Use Deterministic Metadata Models

Use `RuntimeContractMetadata`, `RuntimeRegistryMetadata`, `RuntimeClassificationMetadata`, and
related frozen dataclasses for small serializable maps. Dictionary inputs are sorted for stable
`to_dict()` output.

## Treat Registry As Catalog Only

Use `RuntimeRegistry` to register and look up descriptive entries ordered by
`registration_identifier`. Do not use it to instantiate, activate, execute, or resolve registered
artifacts.

## Preserve Dependency Direction

Runtime Foundation depends on Platform Core and lawfully consumes Interface Foundation and
Integration Foundation. Do not import Phase I cognitive foundations in Runtime consumer code unless
separately authorized.

## Respect The Tripartite Distinction

Do not conflate External Runtime Governance artifacts with Operational Runtime behavior or Universal
Execution Foundation semantics. See [Tripartite Distinction Guide](tripartite-distinction-guide.md).

## Use The Right Serialization Surface

Use artifact `to_dict()` for full deterministic payloads. Use Platform Core `ObjectSerializer.serialize()`
when only inherited object fields are required.

## Stay Inside Certified Boundaries

The certified SDK does not include operational runtime execution, provider integration, persistence,
transport, orchestration, scheduling, invocation, routing, or execution engines as implemented
behavior.

See [Extension Guide](extension-guide.md) for out-of-scope capabilities.
