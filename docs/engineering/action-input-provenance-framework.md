# Action Input and Provenance Framework

## Implementation Summary

GAR-SPRINT-0008 Mission Bravo adds descriptive input and provenance models to `packages.action`.

The implementation is intentionally limited:

- no production package outside `packages/action` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no reference resolution or action execution behavior is introduced

## Public Interface

Import Action input and provenance interfaces from `packages.action`.

```python
from packages.action import ActionInputReference, ActionInputType

reference = ActionInputReference(
    input_type=ActionInputType.DECISION,
    identifier="decision:00000000-0000-0000-0000-000000000001",
)
```

Mission Bravo exports:

- `ActionInputType`
- `ActionInputReference`
- `ActionInputCollection`
- `ActionOrigin`
- `ActionProvenance`
- `validate_action_input_reference`
- `validate_action_input_collection`
- `validate_action_provenance`

## UniversalAction Integration

`UniversalAction` now accepts optional `action_inputs` and `action_provenance` values.

```python
from packages.action import ActionInputCollection, ActionType, UniversalAction

inputs = ActionInputCollection(references=(reference,))
action = UniversalAction(
    action_type=ActionType.TASK,
    action_inputs=inputs,
)
```

Mission Alpha construction remains valid. Optional Bravo fields are emitted only when present.

## Deterministic Payloads

Use `to_dict()` on input references, input collections, provenance records and `UniversalAction`.
Dictionary metadata is stored as sorted tuples internally and emitted deterministically.

## Validation

The module provides local validation helpers returning Platform Core `ValidationResult` values:

- `validate_action_input_reference`
- `validate_action_input_collection`
- `validate_action_provenance`

`UniversalAction.validate()` merges these checks when optional inputs or provenance are present.

## Engineering Boundaries

Do not add reference resolution, provenance evaluation, action execution, scheduling, orchestration,
workflow behavior, optimization, persistence, search, AI behavior, REST APIs, frontend behavior or
autonomous behavior to these modules.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or Decision Foundation to support Action Mission Bravo.

## Verification

Mission Bravo is verified by `tests/test_action_input_provenance_framework.py`, which covers
construction, immutability, deterministic payloads, validation helper behavior, `UniversalAction`
integration, Platform Core serialization compatibility, prior foundation coexistence and absence of
future execution behavior.
