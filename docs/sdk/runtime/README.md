# Runtime Foundation SDK Documentation

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Version And Certification

| Field | Value |
| --- | --- |
| Certification record | [GAR-CERT-S12-001](../../sprints/GAR-SPRINT-0012-runtime-certification.md) — **PASS** |
| Repository baseline | `c0e6433` (Golf governance closure) |
| Supported missions | Alpha, Bravo, Charlie, Delta, Echo, Foxtrot, Golf |
| Verification baseline | 1042 passing tests (`unittest discover tests`) |

This SDK documents the certified Runtime Foundation through Mission Golf. It does not describe
Mission India release artifacts or any capability outside the published implementation baseline.

## Purpose

This documentation set is the developer-facing counterpart to
**[GAR-CERT-S12-001](../../sprints/GAR-SPRINT-0012-runtime-certification.md)** (Golf Certification PASS).
If Golf answers whether the Runtime Foundation implementation is correct, Hotel answers whether
another engineer can successfully build with the published foundation.

The SDK documents the certified Runtime substrate, dual subordination contracts, lifecycle and
boundary model, context classification, validation framework, registry catalog, Platform Core
inheritance, and tripartite distinction implemented in `packages.runtime`.

## SDK Index

| Guide | Purpose |
| --- | --- |
| [Runtime SDK Guide](runtime-sdk-guide.md) | Constitutional and architectural context |
| [Developer Guide](developer-guide.md) | Onboarding, navigation, and stack integration walkthrough |
| [Architecture Guide](architecture-guide.md) | ADR-0013 principles and dependency diagram |
| [Tripartite Distinction Guide](tripartite-distinction-guide.md) | External Runtime Governance vs Operational Runtime vs Universal Execution |
| [API Reference](api-reference.md) | Public exported classes and functions |
| [Best Practices](best-practices.md) | Recommended foundation usage |
| [Extension Guide](extension-guide.md) | Governance workflow for contributors |
| [Practical Examples](practical-examples.md) | Canonical usage patterns |

## Modules Covered

- Runtime Core (Mission Alpha)
- Runtime Contracts (Mission Bravo)
- Runtime Lifecycle and Boundary Model (Mission Charlie)
- Runtime Context Classification (Mission Delta)
- Runtime Validation Framework (Mission Echo)
- Runtime Registry (Mission Foxtrot)
- Runtime Foundation Certification (Mission Golf)

## Platform Boundary

The SDK documentation covers only implemented Runtime Foundation behavior. It does not describe
operational runtime execution, provider integration, transport registration, service location,
dependency injection, plugin discovery, persistence, authentication, authorization, orchestration,
scheduling, invocation, routing, or execution engines as implemented capability.

## Related Authority

- [Runtime Foundation Architecture Overview](../../architecture/runtime/overview.md)
- [Architecture documentation](../../architecture/runtime/README.md)
- [Engineering documentation](../../engineering/runtime/README.md)
