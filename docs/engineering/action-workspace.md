# Action Workspace

## Implementation Summary

GAR-SPRINT-0008 Mission Foxtrot adds a runtime-only `ActionWorkspace` for `UniversalAction`
references.

The implementation is intentionally small:

- no production package outside `packages/action` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no action execution behavior is introduced

## Public Interface

Use `ActionWorkspace` to hold process-local `UniversalAction` references by exact object
identifier.

Supported operations:

- `add(action)`
- `get(action_id)`
- `remove(action_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

`get()` and `remove()` accept either a `UUID` or UUID string. `identifiers()` returns identifiers in
deterministic string order.

## Statistics

`WorkspaceStatistics` provides deterministic `to_dict()` output:

```python
{
    "total_actions": 1,
    "active_actions": 0,
    "archived_actions": 0,
}
```

The model is immutable and descriptive. It records counts only.

## Validation

The module provides local validation helpers:

- `validate_action_reference`
- `validate_action_workspace`
- `validate_workspace_statistics`

These helpers return Platform Core `ValidationResult` values. They validate object type, identifier
consistency and statistics structure.

## Serialization

`ActionWorkspace` intentionally does not expose `to_dict()` and must not be serialized.
`WorkspaceStatistics` is the only Foxtrot model with deterministic `to_dict()` payload support.

## Engineering Boundaries

Do not add action execution, outcome computation, scheduling, orchestration, optimization, reference
resolution, criteria retrieval, search, ranking, persistence, AI behavior, REST APIs, frontend
features or autonomous behavior to this module.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or Decision Foundation to support the workspace.

## Verification

Mission Foxtrot is verified by `tests/test_action_workspace.py`, which covers exact identifier
operations, duplicate rejection, invalid reference rejection, object identity preservation,
deterministic statistics, validation compatibility and coexistence with Platform Core, Memory
Foundation, Knowledge Foundation, Context Foundation, Reasoning Foundation and Decision Foundation.
