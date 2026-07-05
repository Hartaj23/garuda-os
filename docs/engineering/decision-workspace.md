# Decision Workspace

## Implementation Summary

GAR-SPRINT-0007 Mission Foxtrot adds a runtime-only `DecisionWorkspace` for `UniversalDecision`
references.

The implementation is intentionally small:

- no production package outside `packages/decision` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no decision execution behavior is introduced

## Public Interface

Use `DecisionWorkspace` to hold process-local `UniversalDecision` references by exact object
identifier.

Supported operations:

- `add(decision)`
- `get(decision_id)`
- `remove(decision_id)`
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
    "total_decisions": 1,
    "active_decisions": 0,
    "archived_decisions": 0,
}
```

The model is immutable and descriptive. It records counts only.

## Validation

The module provides local validation helpers:

- `validate_decision_reference`
- `validate_decision_workspace`
- `validate_workspace_statistics`

These helpers return Platform Core `ValidationResult` values. They validate object type, identifier
consistency and statistics structure.

## Serialization

`DecisionWorkspace` intentionally does not expose `to_dict()` and must not be serialized.
`WorkspaceStatistics` is the only Foxtrot model with deterministic `to_dict()` payload support.

## Engineering Boundaries

Do not add decision execution, outcome computation, orchestration, optimization, reference
resolution, criteria retrieval, search, ranking, persistence, AI behavior, REST APIs, frontend
features or workflow behavior to this module.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
Reasoning Foundation to support the workspace.

## Verification

Mission Foxtrot is verified by `tests/test_decision_workspace.py`, which covers exact identifier
operations, duplicate rejection, invalid reference rejection, object identity preservation,
deterministic statistics, validation compatibility and coexistence with Platform Core, Memory
Foundation, Knowledge Foundation, Context Foundation and Reasoning Foundation.
