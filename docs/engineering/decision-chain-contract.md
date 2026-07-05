# Decision Chain Contract

## Implementation Summary

GAR-SPRINT-0007 Mission Echo adds descriptive chain contract models to the Decision Foundation.

The implementation is intentionally narrow:

- no existing non-Decision foundation package is modified
- no existing Decision behavior is changed
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no chain execution or orchestration behavior is introduced

## Public Interface

Import Decision chain contract interfaces from `packages.decision`.

```python
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainMetadata,
    DecisionChainType,
    DecisionStepReference,
)
```

## Step References

Use `DecisionStepReference` to record an opaque Decision identifier.

```python
step = DecisionStepReference(
    decision_identifier="decision:00000000-0000-0000-0000-000000000001",
)
```

The identifier is descriptive only. The SDK does not resolve it.

## Chain Records

Use `DecisionChain` to describe ordered Decision references.

```python
chain = DecisionChain(
    chain_type=DecisionChainType.SEQUENTIAL,
    steps=(step,),
)
```

The chain represents relationship structure only. It does not execute.

## Chain Contracts

Use `DecisionChainContract` to group one or more chains into a deterministic contract.

```python
contract = DecisionChainContract(
    chains=(chain,),
)
```

The contract records intent only. It does not orchestrate, execute, resolve, optimize or compute
outcomes.

## Validation

The module provides local validation helpers:

- `validate_decision_chain_metadata`
- `validate_decision_step_reference`
- `validate_decision_chain`
- `validate_decision_chain_contract`

These helpers return Platform Core `ValidationResult` values. They validate structure and metadata
only.

## Serialization

Use `to_dict()` on chain models for deterministic payloads. Platform Core `ObjectSerializer` is
unchanged and remains scoped to inherited Platform Core object fields.

## Engineering Boundaries

Do not add chain execution, reference resolution, decision execution, orchestration, outcome
computation, optimization, planning, workflow behavior, persistence, search, AI behavior, REST
APIs, frontend behavior or autonomous behavior to this contract.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
Reasoning Foundation for Mission Echo.

## Verification

Mission Echo is verified by `tests/test_decision_chain_contract.py`, which covers construction,
immutability, deterministic payloads, validation compatibility, Platform Core compatibility,
foundation coexistence, Decision Foundation compatibility, opaque references and explicit absence
of future behavior.
