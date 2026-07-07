# Integration Foundation SDK Extension Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Constitutional Workflow For Contributors

Integration Foundation extensions must follow the governance chain established by GAR-0018:

```
Constitution (GAR-0018)
      ↓
ADR (ADR-0012 and successors)
      ↓
Sprint (GAR-SPRINT-0011 and successors)
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

Extensions must preserve the Integration Foundation boundary:

- Platform Core remains the source of object identity, lifecycle, validation, and serialization.
- Integration value models remain deterministic and immutable where specified.
- Integration contracts remain subordinate to Interface contracts.
- Validation accepts canonical Integration artifacts only.
- Registry remains a descriptive catalog — not a service locator or execution router.
- Phase I cognitive foundations and Interface Foundation remain unmodified unless separately authorized.

## Additive Documentation Extensions

Documentation may be extended to cover newly approved and implemented Integration Foundation behavior.
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

- runtime execution
- provider integration
- transport registration
- persistence
- orchestration
- scheduling
- authentication
- operational discovery or connectivity

See [Migration Guide](migration-guide.md) for consumption guidance across published baselines.
