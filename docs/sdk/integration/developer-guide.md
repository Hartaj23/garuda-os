# Integration Foundation SDK Developer Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Repository Navigation

| Path | Purpose |
| --- | --- |
| `packages/integration/core/` | Integration Foundation substrate |
| `packages/integration/contracts/` | Integration contracts subordinate to interface contracts |
| `packages/integration/lifecycle/` | Boundary model and artifact lifecycle |
| `packages/integration/relationships/` | Descriptive participant relationship semantics |
| `packages/integration/validation/` | Deterministic artifact evaluation |
| `packages/integration/registry/` | Descriptive participant catalog |
| `docs/architecture/integration/` | Architecture documentation |
| `docs/engineering/integration/` | Engineering documentation |
| `docs/sdk/integration/` | This SDK documentation set |

## Public Import Path

```python
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationRegistry,
    evaluate_integration_artifact,
    evaluate_integration_relationship,
)
```

The authoritative public export list is `packages.integration.__all__`. See
[API Reference](api-reference.md).

## Platform Core Inheritance

Canonical Integration Foundation artifacts inherit Platform Core `CanonicalObject`:

- `IntegrationFoundation`
- `CanonicalIntegrationContract`
- `IntegrationBoundaryModel`
- `IntegrationArtifactLifecycle`
- `CanonicalIntegrationRelationship`
- `IntegrationValidationRecord`
- `IntegrationRegistrationContract`

Use `validate()` for Platform Core validation hooks and `ObjectSerializer.serialize()` for inherited
serialization fields.

## Interface Subordination

Integration contracts must remain subordinate to canonical interface contracts through
`IntegrationContractSubordination`. Use `build_interface_subordination()` to construct lawful links to
`CanonicalInterfaceRequest` or `CanonicalInterfaceResponse` values.

## Cognitive Independence

Integration Foundation production modules depend on Platform Core, Interface Foundation (lawful
consumption only), and other Integration submodules. They do not import Memory, Knowledge, Context,
Reasoning, Decision, Action, or Execution packages.

## Descriptive Usage Model

Integration Foundation types describe architectural metadata. They do not route messages, invoke
providers, execute operational integration, or perform persistence.

## Extension Principles

Approved extensions follow constitutional engineering:

1. Obtain architectural approval before implementation.
2. Extend only within the approved mission scope.
3. Preserve Platform Core inheritance and determinism.
4. Do not introduce provider, runtime, or persistence behavior without separate constitutional authority.

See [Extension Guide](extension-guide.md) for the full governance workflow.

## Onboarding Path

1. Read [Integration SDK Guide](integration-sdk-guide.md) for constitutional context.
2. Read [Quick Start Guide](quick-start-guide.md) for first working patterns.
3. Read [Architecture Guide](architecture-guide.md) for ADR-0012 principles.
4. Use [Practical Examples](practical-examples.md) for constructible patterns.
5. Consult [API Reference](api-reference.md) for symbol details.
6. Review Golf certification evidence in GAR-CERT-S11-001 for verified behavior.
