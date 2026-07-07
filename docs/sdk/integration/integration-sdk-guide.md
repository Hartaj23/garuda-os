# Integration Foundation SDK Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Constitutional Role

The Integration Foundation governs descriptive external-capability architecture subordinate to the
Interface Foundation, as established by [GAR-0018](../../../GAR-0018.md).

The Integration Foundation:

- describes integration participants, contracts, lifecycle, relationships, validation, and registry metadata
- terminates integration variability before Phase I cognitive foundations
- remains technology-neutral and descriptive
- does not perform operational integration, connectivity, or provider invocation

## Architectural Position

[ADR-0012](../../adr/ADR-0012-integration-foundation.md) establishes the Integration Foundation as
descriptive governance for external participation. The published descriptive pipeline is:

```
Interface Foundation (membrane)
    → Integration Contracts (subordination)
    → Lifecycle / Boundary metadata
    → Relationship semantics
    → Validation (evaluate_integration_artifact)
    → Registry catalog (descriptive registration and lookup)
```

The registry records what exists. It does not determine what runs.

## Sprint Mission Map

| Mission | Subsystem | SDK focus |
| --- | --- | --- |
| Alpha | Integration Core | `IntegrationFoundation`, package exports |
| Bravo | Integration Contracts | Subordination to interface contracts |
| Charlie | Lifecycle and Boundary | Boundary exclusivity, artifact lifecycle |
| Delta | Relationships | Descriptive participant relationship semantics |
| Echo | Validation | Deterministic artifact evaluation |
| Foxtrot | Registry | Descriptive participant catalog |
| Golf | Certification | Constitutional compliance evidence |
| Hotel | SDK Documentation | Developer enablement (this documentation set) |

## Certification

Golf Certification recorded **PASS** in GAR-CERT-S11-001. SDK documentation describes only behavior
verified against the published implementation baseline `121365c`.

## Import Path

```python
from packages.integration import CanonicalIntegrationContract, IntegrationRegistry
```

All public symbols are exported from `packages.integration`. See [API Reference](api-reference.md).
