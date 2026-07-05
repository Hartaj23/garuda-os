# Action Chain Contract

## Implementation Summary

GAR-SPRINT-0008 Mission Echo adds the descriptive `packages.action.chain` module.

The implementation is intentionally limited:

- no production package outside `packages/action` is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no chain execution, reference resolution or action execution behavior is introduced

## Public Interface

Import Action chain contract interfaces from `packages.action`.

```python
from packages.action import ActionChain, ActionChainType

chain = ActionChain(chain_type=ActionChainType.SEQUENTIAL)
```

Mission Echo exports:

- `ActionChainType`
- `ActionChainMetadata`
- `ActionStepReference`
- `ActionChain`
- `ActionChainContract`
- `validate_action_chain_metadata`
- `validate_action_step_reference`
- `validate_action_chain`
- `validate_action_chain_contract`

## Deterministic Payloads

Use `to_dict()` on `ActionStepReference`, `ActionChain` and `ActionChainContract`. Metadata
dictionaries are stored as sorted tuples internally and emitted deterministically.

## Validation

The module provides local validation helpers returning Platform Core `ValidationResult` values.
They validate chain type, step reference identifier, metadata, contract version and contract chain
structure.

## Engineering Boundaries

Do not add chain execution, reference resolution, action execution, scheduling, orchestration,
workflow behavior, optimization, persistence, search, AI behavior, REST APIs, frontend behavior or
autonomous behavior to this module.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or Decision Foundation to support Action Mission Echo.

## Verification

Mission Echo is verified by `tests/test_action_chain_contract.py`, which covers construction,
immutability, deterministic payloads, validation helper behavior, opaque step references, Platform
Core serialization compatibility, prior foundation coexistence, Action Foundation compatibility and
absence of future execution behavior.
