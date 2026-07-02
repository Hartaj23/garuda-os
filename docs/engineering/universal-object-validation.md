# Universal Object Validation Engineering Notes

## Implementation summary

The validation framework resides in [packages/objects](../../packages/objects), primarily in
`packages/objects/validation.py`.

## Design notes

- `ValidationSeverity` defines platform severity levels.
- `ValidationCategory` defines universal object validation categories.
- `ValidationError` is the atomic finding model.
- `ValidationResult` aggregates findings and exposes `is_valid`.
- Helper functions validate universal object identity, metadata, lifecycle, behavior,
  relationships, schema, and version concerns.
- `GarudaObject.validate()` returns a `ValidationResult` while preserving existing hook
  execution semantics.

## Hook compatibility

Validation hooks may:

- Return `None`.
- Return a `ValidationError`.
- Return a `ValidationResult`.
- Raise an exception.

Raised exceptions are not converted into validation results. This preserves existing
exception-based hook behavior.

## Testing expectations

Tests should cover the validation models, helper functions, hook integration, and explicit
mission boundaries. Tests must not introduce business, trading, portfolio, AI, persistence,
API, frontend, workflow, knowledge graph, or memory validation behavior.
