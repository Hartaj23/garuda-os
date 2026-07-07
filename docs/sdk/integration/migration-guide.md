# Integration Foundation SDK Migration Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Baseline Policy

Treat `121365c` as the authoritative Integration Foundation SDK baseline. Consumer code should pin
to published mission commits or later Integration Foundation release tags authorized by sprint
closure documentation.

## Consuming Published Modules Incrementally

If your application only needs a subset of the Integration Foundation, import only the required
public symbols from `packages.integration`:

| Need | Start with |
| --- | --- |
| Foundation substrate only | `IntegrationFoundation` |
| Contract governance | `CanonicalIntegrationContract`, `build_interface_subordination` |
| Lifecycle metadata | `IntegrationArtifactLifecycle`, `IntegrationBoundaryModel` |
| Relationship semantics | `CanonicalIntegrationRelationship` |
| Validation | `evaluate_integration_artifact`, `IntegrationValidationPolicy` |
| Registry catalog | `IntegrationRegistry`, `compose_integration_registry_entry` |

Do not depend on undocumented internal module paths.

## Validation Policy Migration

When tightening validation policies:

1. Preserve `policy_identifier` and increment `policy_version`.
2. Add version compatibility rules explicitly through `IntegrationVersionCompatibilityRule`.
3. Re-run `evaluate_integration_artifact()` and compare deterministic outcomes.

## Registry Entry Migration

When updating registry entries:

1. Create a new `registration_identifier` for materially different catalog semantics.
2. Keep participant descriptors aligned with `CANONICAL_INTEGRATION_ARTIFACT_TYPES`.
3. Validate composition with `validate_integration_registry_artifact_composition()` before registration.

## Interface Contract Changes Upstream

Integration contracts remain subordinate to Interface contracts. If Interface contract identifiers
change upstream, update `IntegrationContractSubordination` through `build_interface_subordination()`
rather than mutating subordination fields in place.

## Future-Proofing Rules

- Import from `packages.integration` public exports only.
- Avoid coupling to mission-internal validation hook names.
- Treat all Integration artifacts as immutable descriptive records after construction.
- Do not assume operational integration behavior will appear in future patch releases without new
  constitutional authority.

## Related Documents

- [Extension Guide](extension-guide.md)
- [Troubleshooting Guide](troubleshooting-guide.md)
