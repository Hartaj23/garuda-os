# Runtime Foundation SDK Extension Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Constitutional Workflow For Contributors

Runtime Foundation extensions must follow the governance chain established by GAR-0019:

```
Constitution (GAR-0019)
      ↓
ADR (ADR-0013 and successors)
      ↓
Sprint (GAR-SPRINT-0012 and successors)
      ↓
Mission (Alpha, Bravo, …)
      ↓
Implementation (approved scope only)
      ↓
Certification (Mission Golf pattern)
```

No capability enters the repository without passing through this chain. Documentation extensions
describe only behavior that has completed this workflow.

## Extension Principles

Extensions must preserve the Runtime Foundation boundary:

- Platform Core remains the source of object identity, lifecycle, validation, and serialization.
- Runtime value models remain deterministic and immutable where specified.
- Runtime contracts remain subordinate to both Integration and Interface contracts.
- Validation accepts canonical Runtime artifacts only.
- Registry remains a descriptive catalog — not a service locator or execution router.
- Phase I cognitive foundations, Interface Foundation, and Integration Foundation remain unmodified
  unless separately authorized.

## Additive Documentation Extensions

Documentation may be extended to cover newly approved and implemented Runtime Foundation behavior.
Do not document proposed behavior as available.

## Additive Model Extensions

Future model additions should follow the existing pattern:

- `@dataclass(frozen=True, slots=True)` for shared value models
- explicit enum values for platform-neutral categories
- deterministic `to_dict()` payloads
- validation helpers returning Platform Core `ValidationResult`
- `CanonicalObject` inheritance for canonical artifacts
- explicit architectural invariants in primary model docstrings

## Out-Of-Scope Extensions

The following capabilities are not implemented and must not be treated as available SDK behavior:

- operational runtime execution
- provider integration
- transport registration
- persistence
- orchestration
- scheduling
- invocation
- routing
- execution engines
- authentication
- operational discovery or connectivity

See [Tripartite Distinction Guide](tripartite-distinction-guide.md) for constitutional boundary
definitions.

## Architectural Change Protocol

Runtime Foundation architectural changes require GAR-0016 Architectural Change Protocol approval
before implementation begins.
