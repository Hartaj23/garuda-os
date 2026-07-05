# Universal Action Framework

## Implementation Summary

GAR-SPRINT-0008 Mission Alpha adds the `packages.action` package and the `UniversalAction`
platform object.

The implementation is intentionally limited:

- no production package outside `packages/action` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no action execution behavior is introduced

## Public Interface

Import Action Foundation interfaces from `packages.action`.

```python
from packages.action import ActionType, UniversalAction

action = UniversalAction(action_type=ActionType.TASK)
```

Mission Alpha exports:

- `UniversalAction`
- `ActionType`
- `ActionState`
- `ActionOutcome`
- `ActionConfidence`
- `ActionMetadata`
- `validate_action`

## Deterministic Payloads

Use `UniversalAction.to_dict()` for the full deterministic Action payload.

```python
payload = action.to_dict()

assert payload["object_type"] == "UniversalAction"
assert payload["action_type"] == "task"
```

Use Platform Core `ObjectSerializer` only for inherited Platform Core fields.

## Validation

`UniversalAction` registers `validate_action` through Platform Core validation hooks. The helper
returns Platform Core `ValidationResult` values and checks Action-specific type, state, outcome,
confidence and metadata fields.

## Confidence And Metadata

`ActionConfidence` records confidence about the Action record. It does not determine truth or
execute behavior.

`ActionMetadata` is immutable and deterministic. It should contain descriptive metadata only.

## Engineering Boundaries

Do not add action execution, scheduling, orchestration, workflow behavior, outcome evaluation,
optimization, persistence, search, AI behavior, REST APIs, frontend behavior or autonomous behavior
to this package.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or Decision Foundation to support Action Mission Alpha.

## Verification

Mission Alpha is verified by `tests/test_universal_action_framework.py`, which covers construction,
immutability, deterministic payloads, Platform Core interoperability, prior foundation coexistence
and absence of future execution behavior.
