# Integration Foundation SDK Coding Conventions

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Import Conventions

Import from the public package surface only:

```python
from packages.integration import CanonicalIntegrationContract
```

Do not import from internal submodule paths such as `packages.integration.contracts.contract` in
consumer code unless you are implementing approved Integration Foundation scope.

## Identifier Conventions

Use stable, technology-neutral identifiers:

- participant identifiers: `participant:<uuid>`
- registration identifiers: `registration:<scope>:v<version>`
- policy identifiers: `<artifact-scope>:v<version>`

Avoid embedding protocol names, hostnames, credentials, or provider-specific tokens.

## Validation Conventions

1. Construct the artifact.
2. Call artifact `validate()` for hook validation.
3. Call `evaluate_integration_artifact()` when policy-based certification is required.
4. Inspect Platform Core `ValidationResult` deterministically — do not infer business semantics from error text.

## Metadata Conventions

Prefer frozen metadata dataclasses over raw dictionaries at Integration boundaries. When dictionaries
are used for convenience, expect deterministic sorting during `__post_init__`.

## Registry Conventions

Compose registry entries with `compose_integration_registry_entry()`. Align participant descriptors
with published artifact types using `validate_integration_registry_artifact_composition()` when linking
registry metadata to live artifacts.

## Serialization Conventions

- Full record payloads: `artifact.to_dict()`
- Inherited Platform Core fields only: `ObjectSerializer.serialize(artifact)`
- Validation outcomes: `validation_result_to_outcome(result).to_dict()`

## Testing Conventions

Use mission-aligned fixtures with explicit UUIDs and fixed timestamps. Verify determinism by comparing
repeated `to_dict()` outputs.

## Prohibited Patterns

- Treating Integration Foundation as an operational integration runtime
- Passing non-integration artifacts to `evaluate_integration_artifact()`
- Using registry lookup results as execution handles
- Modifying Phase I or Interface packages from Integration consumer code
