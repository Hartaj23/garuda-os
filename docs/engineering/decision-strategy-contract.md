# Decision Strategy Contract

## Implementation Summary

GAR-SPRINT-0007 Mission Delta adds descriptive strategy contract models to the Decision Foundation.

The implementation is intentionally narrow:

- no existing non-Decision foundation package is modified
- no existing Decision behavior is changed
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no strategy execution behavior is introduced

## Public Interface

Import Decision strategy contract interfaces from `packages.decision`.

```python
from packages.decision import (
    DecisionStrategy,
    DecisionStrategyContract,
    DecisionStrategyMetadata,
    DecisionStrategyType,
)
```

## Strategy Records

Use `DecisionStrategy` to describe a strategy.

```python
strategy = DecisionStrategy(
    strategy_type=DecisionStrategyType.ANALYTICAL,
    name="evidence-review",
)
```

The strategy is descriptive only. It does not execute.

## Strategy Contracts

Use `DecisionStrategyContract` to group one or more strategies into a deterministic contract.

```python
contract = DecisionStrategyContract(
    strategies=(strategy,),
)
```

The contract records intent only. It does not evaluate, rank, select, optimize or execute
strategies.

## Validation

The module provides local validation helpers:

- `validate_decision_strategy_metadata`
- `validate_decision_strategy`
- `validate_decision_strategy_contract`

These helpers return Platform Core `ValidationResult` values. They validate structure and metadata
only.

## Serialization

Use `to_dict()` on strategy models for deterministic payloads. Platform Core `ObjectSerializer`
is unchanged and remains scoped to inherited Platform Core object fields.

## Engineering Boundaries

Do not add strategy execution, strategy evaluation, decision engine behavior, decision execution,
outcome computation, optimization, planning, workflow behavior, orchestration, persistence, search,
AI behavior, REST APIs, frontend behavior or autonomous behavior to this contract.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
Reasoning Foundation for Mission Delta.

## Verification

Mission Delta is verified by `tests/test_decision_strategy_contract.py`, which covers construction,
immutability, deterministic payloads, validation compatibility, Platform Core compatibility,
foundation coexistence, Decision Foundation compatibility and explicit absence of future behavior.
