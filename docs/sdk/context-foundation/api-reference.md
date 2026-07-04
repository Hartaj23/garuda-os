# Context Foundation SDK API Reference

## Import Path

All public Context Foundation SDK interfaces are exported from `packages.context`.

```python
from packages.context import ContextType, ContextWorkspace, UniversalContext
```

## Universal Context

### `UniversalContext`

Platform-level Context object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `context_type`
- `context_state`
- `context_confidence`
- `context_metadata`
- `context_source`
- `context_scope`
- inherited Platform Core object fields

Public properties:

- `context_type`
- `context_state`
- `context_confidence`
- `context_metadata`
- `context_source`
- `context_scope`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `ContextType`

Enum values:

- `conversational`
- `operational`
- `analytical`
- `environmental`
- `temporal`

### `ContextState`

Enum values:

- `draft`
- `assembled`
- `validated`
- `active`
- `archived`

### `ContextConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `ContextMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Source And Scope

### `ContextSourceType`

Enum values:

- `memory`
- `knowledge`
- `user_input`
- `system_state`
- `external_reference`

### `ContextSource`

Frozen dataclass fields:

- `source_type`
- `source_identifier`
- `created_at`
- `source_metadata`

Public methods:

- `to_dict()`

### `ContextScopeType`

Enum values:

- `local`
- `session`
- `task`
- `workflow`
- `global`

### `ContextScope`

Frozen dataclass fields:

- `scope_type`
- `boundary_identifier`
- `lifetime_metadata`
- `scope_metadata`

Public methods:

- `to_dict()`

## Composition Contract

### `CompositionType`

Enum values:

- `sequential`
- `parallel`
- `layered`
- `hierarchical`
- `grouped`

### `CompositionMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ContextComposition`

Frozen dataclass fields:

- `composition_type`
- `context_identifiers`
- `composition_metadata`

Public methods:

- `to_dict()`

### `ContextCompositionContract`

Frozen dataclass fields:

- `supported_composition_types`
- `supported_metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Selection Contract

### `SelectionType`

Enum values:

- `exact_identifier`
- `source_based`
- `scope_based`
- `type_based`
- `composition_based`

### `SelectionMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `SelectionCriterion`

Frozen dataclass fields:

- `criterion_name`
- `operator`
- `criterion_value`

Public methods:

- `to_dict()`

### `ContextSelectionRequest`

Frozen dataclass fields:

- `selection_type`
- `criteria`
- `metadata`

Public methods:

- `to_dict()`

### `ContextSelectionContract`

Frozen dataclass fields:

- `supported_selection_types`
- `supported_criteria`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Workspace

### `WorkspaceStatistics`

Frozen dataclass fields:

- `total_contexts`
- `created_at`
- `last_modified_at`

Public methods:

- `to_dict()`

### `ContextWorkspace`

Runtime-only process-local container for `UniversalContext` references.

Public methods:

- `add(context)`
- `get(context_id)`
- `remove(context_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

## Validation Helpers

Public validation helpers:

- `validate_context`
- `validate_context_source`
- `validate_context_scope`
- `validate_composition_metadata`
- `validate_context_composition`
- `validate_context_composition_contract`
- `validate_selection_metadata`
- `validate_selection_criterion`
- `validate_context_selection_request`
- `validate_context_selection_contract`
- `validate_context_reference`
- `validate_workspace_statistics`
- `validate_context_workspace`

Validation helpers return Platform Core `ValidationResult`.
