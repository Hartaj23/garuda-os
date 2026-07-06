# Interface Foundation SDK Extension Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## Constitutional Workflow For Contributors

Interface Foundation extensions must follow the governance chain established by GAR-0017:

```
Constitution (GAR-0017)
      ↓
ADR (ADR-0011 and successors)
      ↓
Sprint (GAR-SPRINT-0010 and successors)
      ↓
Mission (Alpha, Bravo, …)
      ↓
Implementation (approved scope only)
      ↓
Certification (Mission Golf pattern)
```

No capability enters the repository without passing through this chain. Documentation extensions
describe only behavior that has completed this workflow.

Architectural changes that exceed sprint scope require the GAR-0016 Architecture Change Proposal
process before any implementation begins.

## Extension Principles

Extensions must preserve the Interface Foundation boundary:

- Platform Core remains the source of object identity, lifecycle, validation, and serialization.
- Interface value models remain deterministic and immutable where specified.
- Translation remains inbound-only unless a future approved mission authorizes outbound behavior.
- Validation accepts canonical Interface artifacts only.
- Registry remains a descriptive catalog — not a service locator or execution router.
- Phase I cognitive foundations remain unmodified unless separately authorized.

## Additive Documentation Extensions

Documentation may be extended to cover newly approved and implemented Interface Foundation behavior.
Do not document proposed behavior as available.

## Additive Model Extensions

Future model additions should follow the existing pattern:

- `@dataclass(frozen=True, slots=True)` for shared value models
- explicit enum values for platform-neutral categories
- deterministic `to_dict()` payloads
- validation helpers returning Platform Core `ValidationResult`
- `CanonicalObject` inheritance for canonical artifacts
- no custom serializer outside Platform Core

## Registry Extensions

The implemented `InterfaceRegistry` supports descriptive catalog operations only. Do not extend it into
a service locator, dependency injection container, plugin loader, provider registry, or execution router
without separate architecture approval.

## Cross-Foundation Extensions

Interface models may reference opaque identifiers associated with other foundations. Do not embed
`UniversalMemory`, `UniversalKnowledge`, `UniversalContext`, `UniversalReasoning`, `UniversalDecision`,
`UniversalAction`, or `UniversalExecution` objects in Interface contracts.

## Out-Of-Scope Extensions

The following capabilities are not implemented and must not be treated as available SDK behavior:

- runtime execution
- provider integration
- transport registration
- service location
- dependency injection
- plugin discovery
- persistence
- authentication or authorization
- REST or HTTP APIs
- MCP integration
- OpenAI or LLM provider integration
- orchestration or scheduling
- outbound translation
- workflow engines

## Platform Boundary

See [README](README.md) for the complete platform boundary statement.
