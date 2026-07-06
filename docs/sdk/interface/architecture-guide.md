# Interface Foundation SDK Architecture Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## ADR-0011 Principles

| Principle | SDK realization |
| --- | --- |
| Exclusive Boundary | `InterfaceBoundaryModel` with single-membrane exclusivity |
| Technology Neutrality | No provider or transport types in public API |
| Canonical Communication | `CanonicalInterfaceRequest`, `CanonicalInterfaceResponse` |
| Architectural Translation | `normalize_to_canonical_payload` (inbound only) |
| Deterministic Boundary | `evaluate_interface_artifact`, deterministic registry lookup |
| Cognitive Independence | No Phase I imports in Interface production modules |
| Variability Containment | External metadata terminates at translation layer |
| Platform Core Inheritance | All canonical artifacts inherit `CanonicalObject` |

## Catalog vs Container

| Component | Role |
| --- | --- |
| Translation | Normalizes external representations to canonical payloads |
| Validation | Evaluates canonical artifacts against policies |
| Registry | Describes registered artifacts — does not instantiate or execute |
| Lifecycle | Records descriptive boundary and lifecycle metadata |

## Submodule Layout

```
packages/interface/
    core.py                 # InterfaceFoundation
    contracts/              # Canonical request/response
    lifecycle/              # Boundary and artifact lifecycle
    translation/            # External representation normalization
    validation/             # Artifact evaluation
    registry/               # Descriptive catalog
```

## Out of Scope

The implemented architecture does not include runtime execution, provider registration, persistence,
REST endpoints, orchestration, or outbound translation. See [Extension Guide](extension-guide.md).
