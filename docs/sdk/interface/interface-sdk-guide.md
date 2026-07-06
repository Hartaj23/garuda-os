# Interface Foundation SDK Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## Constitutional Role

The Interface Foundation is the exclusive constitutional boundary between External Systems and the
Internal Cognitive Foundations, as established by [GAR-0017](../../../GAR-0017.md) Article VII.

The Interface Foundation:

- governs communication across the Constitutional Membrane
- terminates external variability before it reaches cognitive foundations
- remains technology-neutral and descriptive
- does not perform cognition, execution, or provider integration

## Architectural Position

[ADR-0011](../../adr/ADR-0011-interface-foundation.md) establishes the Interface Foundation as the
architectural realization of the Constitutional Membrane. The inbound pipeline implemented in Sprint
0010 is:

```
ExternalRepresentation
    → Translation (normalize_to_canonical_payload)
    → Validation (evaluate_interface_artifact)
    → Lifecycle / Boundary metadata
    → Registry catalog (descriptive registration and lookup)
```

The registry records what exists. It does not determine what runs.

## Sprint Mission Map

| Mission | Subsystem | SDK focus |
| --- | --- | --- |
| Alpha | Interface Core | `InterfaceFoundation`, package exports |
| Bravo | Canonical Contracts | Request/response contracts |
| Charlie | Lifecycle and Boundary | Boundary exclusivity, artifact lifecycle |
| Delta | Translation | Inbound normalization |
| Echo | Validation | Deterministic artifact evaluation |
| Foxtrot | Registry | Descriptive catalog |
| Golf | Certification | Constitutional compliance evidence |

## Certification

Mission Golf certified all ten scenarios documented in
[GAR-SPRINT-0010 Interface Certification](../../sprints/GAR-SPRINT-0010-interface-certification.md).
SDK documentation describes only behavior verified by that certification record.

## Import Path

```python
from packages.interface import CanonicalInterfaceRequest, InterfaceRegistry
```

All public symbols are exported from `packages.interface`. See [API Reference](api-reference.md).
