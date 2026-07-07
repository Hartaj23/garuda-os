# Integration Foundation SDK Documentation

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Purpose

This documentation set is the developer-facing counterpart to
**[GAR-CERT-S11-001](../../sprints/GAR-SPRINT-0011-integration-certification.md)** (Golf Certification PASS).
If Golf answers whether the Integration Foundation implementation is correct, Hotel answers whether
another engineer can successfully build with the published foundation.

The SDK documents the certified Integration substrate, contracts, lifecycle and boundary model,
relationship framework, validation framework, registry catalog, Platform Core inheritance, and
Interface subordination implemented in `packages.integration`.

## SDK Index

| Guide | Purpose |
| --- | --- |
| [Integration SDK Guide](integration-sdk-guide.md) | Constitutional and architectural context |
| [Quick Start Guide](quick-start-guide.md) | New developer onboarding |
| [Developer Guide](developer-guide.md) | End-to-end usage patterns |
| [Architecture Guide](architecture-guide.md) | ADR-0012 principles and dependency diagram |
| [API Reference](api-reference.md) | Public exported classes and functions |
| [Best Practices](best-practices.md) | Recommended foundation usage |
| [Coding Conventions](coding-conventions.md) | Foundation usage standards |
| [Extension Guide](extension-guide.md) | Governance workflow for contributors |
| [Migration Guide](migration-guide.md) | Future-proof consumption guidance |
| [Troubleshooting Guide](troubleshooting-guide.md) | Common integration issues |
| [Practical Examples](practical-examples.md) | Canonical usage patterns |

## Modules Covered

- Integration Core (Mission Alpha)
- Integration Contracts (Mission Bravo)
- Integration Lifecycle and Boundary Model (Mission Charlie)
- Integration Relationship Framework (Mission Delta)
- Integration Validation Framework (Mission Echo)
- Integration Registry (Mission Foxtrot)
- Integration Foundation Certification (Mission Golf)

## Platform Boundary

The SDK documentation covers only implemented Integration Foundation behavior. It does not describe
runtime execution, provider integration, transport registration, service location, dependency
injection, plugin discovery, persistence, authentication, authorization, REST APIs, orchestration,
scheduling, or operational integration as implemented capability.

## Related Authority

- [Integration Foundation Architecture Diagram](../../architecture/integration/integration-foundation-architecture-diagram.md)
- [Architecture documentation](../../architecture/integration/README.md)
- [Engineering documentation](../../engineering/integration/README.md)
