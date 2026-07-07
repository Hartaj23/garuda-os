# Runtime Foundation SDK Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Constitutional Role

The Runtime Foundation governs descriptive External Runtime Governance subordinate to the Integration
Foundation and Interface Foundation, as established by [GAR-0019](../../../GAR-0019.md).

The Runtime Foundation:

- describes runtime contracts, lifecycle, context classification, validation, and registry metadata
- terminates runtime variability before Phase I cognitive foundations
- remains technology-neutral and descriptive
- does not perform operational runtime execution, invocation, scheduling, or provider orchestration

See [Tripartite Distinction Guide](tripartite-distinction-guide.md) for the constitutional separation
between External Runtime Governance, Operational Runtime, and Universal Execution Foundation.

## Architectural Position

[ADR-0013](../../adr/ADR-0013-runtime-foundation.md) establishes the Runtime Foundation as
descriptive governance for external runtime context. The published descriptive pipeline is:

```
Interface Foundation (membrane)
    → Integration Contracts (subordination)
    → Runtime Contracts (dual subordination)
    → Lifecycle / Boundary metadata
    → Context classification
    → Validation (evaluate_runtime_artifact)
    → Registry catalog (descriptive registration and lookup)
```

The registry records what exists. It does not determine what runs.

## Sprint Mission Map

| Mission | Subsystem | Implementation commit | SDK focus |
| --- | --- | --- | --- |
| Alpha | Runtime Core | `a33f2d1` | `RuntimeFoundation`, package exports |
| Bravo | Runtime Contracts | `626e7f3` | Dual subordination to Integration and Interface |
| Charlie | Lifecycle and Boundary | `c4c203b` | Boundary exclusivity, artifact lifecycle |
| Delta | Context Classification | `820bc2a` | Pure deterministic classification evaluation |
| Echo | Validation | `78c365d` | Deterministic artifact evaluation |
| Foxtrot | Registry | `e9de697` | Descriptive context catalog |
| Golf | Certification | `d6dd58f` | Constitutional compliance evidence |
| Hotel | SDK Documentation | — | Developer enablement (this documentation set) |

## Certification

Golf Certification recorded **PASS** in GAR-CERT-S12-001. SDK documentation describes only behavior
verified against the published implementation baseline `c0e6433`.

## Import Path

```python
from packages.runtime import CanonicalRuntimeContract, RuntimeRegistry
```

All public symbols are exported from `packages.runtime`. See [API Reference](api-reference.md).
