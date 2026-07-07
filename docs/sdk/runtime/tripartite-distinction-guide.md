# Runtime Foundation SDK Tripartite Distinction Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Purpose

GAR-0019 and ADR-0013 require a constitutional distinction between three runtime-related concepts.
This guide documents how each concept appears in the certified Runtime Foundation SDK.

## External Runtime Governance

**External Runtime Governance** is what the Runtime Foundation **is**.

The certified SDK in `packages.runtime` implements descriptive External Runtime Governance only:

- `RuntimeFoundation` and related core substrate (Mission Alpha)
- `CanonicalRuntimeContract` with dual subordination (Mission Bravo)
- Lifecycle and boundary metadata (Mission Charlie)
- Context classification records (Mission Delta)
- Validation framework (Mission Echo)
- Registry catalog (Mission Foxtrot)

These artifacts describe architectural metadata. They do not invoke, schedule, route, or execute
anything.

**Related certification scenario(s):** 1, 6, 7, 8, 14

## Operational Runtime

**Operational Runtime** is what the Runtime Foundation **is not**.

Operational Runtime would include execution engines, invocation, scheduling, routing, provider
integration, transport registration, and service location. None of these capabilities are
implemented in `packages.runtime`.

The validation framework enforces this boundary through:

- `validate_runtime_operational_runtime_exclusion()`
- `FORBIDDEN_OPERATIONAL_OBJECT_PREFIXES`

Do not treat Runtime Foundation types as executors, orchestrators, or service locators.

**Related certification scenario(s):** 13

## Universal Execution Foundation

**Universal Execution Foundation** is Phase I cognitive execution — a separate foundation that the
Runtime Foundation must not conflate or extend.

Key distinctions:

- `RuntimeFoundation` is not `UniversalExecution`
- Runtime production modules do not import `packages.execution`
- Runtime artifacts describe governance metadata; execution artifacts describe cognitive action

The certified stack preserves cognitive independence: Runtime Foundation depends on Platform Core,
Interface Foundation, and Integration Foundation through lawful import-only consumption. Phase I
cognitive foundations remain separate.

**Related certification scenario(s):** 5, 12, 14

## Summary Table

| Concept | Runtime Foundation treatment | SDK consumer rule |
| --- | --- | --- |
| External Runtime Governance | Sole authorized scope — descriptive artifacts | Use Runtime SDK types for metadata |
| Operational Runtime | Explicitly excluded — no execution semantics | Do not expect invocation or scheduling |
| Universal Execution Foundation | Phase I execution — separate foundation | Do not conflate with Runtime types |

## Related Documents

- [Runtime Foundation Architecture Overview](../../architecture/runtime/overview.md)
- [Architecture Guide](architecture-guide.md)
- [GAR-CERT-S12-001](../../sprints/GAR-SPRINT-0012-runtime-certification.md)
