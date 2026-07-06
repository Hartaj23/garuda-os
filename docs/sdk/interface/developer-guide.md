# Interface Foundation SDK Developer Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## Repository Navigation

| Path | Purpose |
| --- | --- |
| `packages/interface/core.py` | Interface Foundation substrate |
| `packages/interface/contracts/` | Canonical request and response contracts |
| `packages/interface/lifecycle/` | Boundary model and artifact lifecycle |
| `packages/interface/translation/` | External representation normalization |
| `packages/interface/validation/` | Deterministic artifact evaluation |
| `packages/interface/registry/` | Descriptive registration catalog |
| `docs/architecture/interface/` | Architecture documentation |
| `docs/engineering/interface/` | Engineering documentation |
| `docs/sdk/interface/` | This SDK documentation set |

## Public Import Path

```python
from packages.interface import (
    CanonicalInterfaceRequest,
    InterfaceRegistry,
    normalize_to_canonical_payload,
    evaluate_interface_artifact,
)
```

The authoritative public export list is `packages.interface.__all__`. See
[API Reference](api-reference.md).

## Platform Core Inheritance

Canonical Interface Foundation artifacts inherit Platform Core `CanonicalObject`:

- `InterfaceFoundation`
- `CanonicalInterfaceRequest`
- `CanonicalInterfaceResponse`
- `InterfaceBoundaryModel`
- `InterfaceArtifactLifecycle`
- `CanonicalTranslationContract`
- `InterfaceValidationRecord`
- `InterfaceRegistrationContract`

Use `validate()` for Platform Core validation hooks and `ObjectSerializer.serialize()` for inherited
serialization fields.

## Cognitive Independence

Interface Foundation production modules depend on Platform Core and other Interface submodules only.
They do not import Memory, Knowledge, Context, Reasoning, Decision, Action, or Execution packages.

Phase I foundations may coexist in the same process but are not coupled at the Interface layer.

## Extension Principles

Approved extensions follow constitutional engineering:

1. Obtain architectural approval before implementation.
2. Extend only within the approved mission scope.
3. Preserve Platform Core inheritance and determinism.
4. Do not introduce provider, runtime, or persistence behavior without separate constitutional authority.

See [Extension Guide](extension-guide.md) for the full governance workflow.

## Onboarding Path

1. Read [Interface SDK Guide](interface-sdk-guide.md) for constitutional context.
2. Read [Architecture Guide](architecture-guide.md) for ADR-0011 principles.
3. Use [Practical Examples](practical-examples.md) for constructible patterns.
4. Consult [API Reference](api-reference.md) for symbol details.
5. Review [Certification record](../../sprints/GAR-SPRINT-0010-interface-certification.md) for verified behavior.
