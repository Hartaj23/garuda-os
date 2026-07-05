# Action Strategy Contract

## Implementation Summary

GAR-SPRINT-0008 Mission Delta adds the descriptive `packages.action.strategy` module.

The implementation is intentionally limited:

- no production package outside `packages/action` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no strategy execution or action execution behavior is introduced

## Public Interface

Import Action strategy contract interfaces from `packages.action`.

```python
from packages.action import ActionStrategy, ActionStrategyType

strategy = ActionStrategy(
    strategy_type=ActionStrategyType.PROCEDURAL,
    name="operator-review",
)
```

Mission Delta exports:

- `ActionStrategyType`
- `ActionStrategyMetadata`
- `ActionStrategy`
- `ActionStrategyContract`
- `validate_action_strategy_metadata`
- `validate_action_strategy`
- `validate_action_strategy_contract`

## Deterministic Payloads

Use `to_dict()` on `ActionStrategy` and `ActionStrategyContract`. Metadata dictionaries are stored
as sorted tuples internally and emitted deterministically.

## Validation

The module provides local validation helpers returning Platform Core `ValidationResult` values.
They validate strategy type, name, description, metadata, contract version and contract strategy
structure.

## Engineering Boundaries

Do not add strategy execution, strategy evaluation, action execution, scheduling, orchestration,
workflow behavior, optimization, persistence, search, AI behavior, REST APIs, frontend behavior or
autonomous behavior to this module.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or Decision Foundation to support Action Mission Delta.

## Verification

Mission Delta is verified by `tests/test_action_strategy_contract.py`, which covers construction,
immutability, deterministic payloads, validation helper behavior, Platform Core serialization
compatibility, prior foundation coexistence, Action Foundation compatibility and absence of future
execution behavior.
