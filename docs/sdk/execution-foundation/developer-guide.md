# Execution Foundation Developer Guide

## Create Universal Execution

```python
from packages.execution import ExecutionType, UniversalExecution

execution = UniversalExecution(
    execution_type=ExecutionType.ACTION,
)
```

`UniversalExecution` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Use Outcome, Confidence, And Metadata

```python
from packages.execution import (
    ExecutionConfidence,
    ExecutionMetadata,
    ExecutionOutcome,
    ExecutionState,
    ExecutionType,
    UniversalExecution,
)

execution = UniversalExecution(
    execution_type=ExecutionType.REVIEW,
    execution_state=ExecutionState.READY,
    execution_outcome=ExecutionOutcome.UNKNOWN,
    execution_confidence=ExecutionConfidence(level="high", rationale="reviewed"),
    execution_metadata=ExecutionMetadata(values={"domain": "platform"}),
)
```

`ExecutionConfidence` records confidence about the Execution record. It does not compute truth, execute
work, schedule tasks, or determine an outcome.

## Add Inputs And Provenance

```python
from packages.execution import (
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionOrigin,
    ExecutionProvenance,
    ExecutionType,
    UniversalExecution,
)

inputs = ExecutionInputCollection(
    references=(
        ExecutionInputReference(
            input_type=ExecutionInputType.ACTION,
            identifier="action:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = ExecutionProvenance(
    origin=ExecutionOrigin.ACTION,
    input_references=inputs.references,
)
execution = UniversalExecution(
    execution_type=ExecutionType.ACTION,
    execution_inputs=inputs,
    execution_provenance=provenance,
)
```

Inputs and provenance are descriptive. They do not resolve identifiers or evaluate provenance.

## Validate Execution

```python
result = execution.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Execution-specific checks through the
existing validation hook path.

## Serialize Execution

```python
payload = execution.to_dict()

assert payload["object_type"] == "UniversalExecution"
assert payload["execution_type"] == "action"
```

`UniversalExecution.to_dict()` is the deterministic Execution payload.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(execution)

assert core_payload["object_type"] == "UniversalExecution"
assert core_payload["object_id"] == str(execution.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalExecution.to_dict()`.

## Use Strategy Contracts

```python
from packages.execution import ExecutionStrategy, ExecutionStrategyType

strategy = ExecutionStrategy(
    strategy_type=ExecutionStrategyType.MANUAL,
    name="operator-review",
)
```

Strategy contracts describe strategy intent. They do not execute strategies or optimize executions.

## Use Chain Contracts

```python
from packages.execution import ExecutionChain, ExecutionChainType

chain = ExecutionChain(
    chain_type=ExecutionChainType.SEQUENTIAL,
)
```

Chain contracts describe chain structure. They do not execute chains or resolve step references.

## Use The Execution Workspace

```python
from packages.execution import ExecutionWorkspace

workspace = ExecutionWorkspace()
workspace.add(execution)

same_execution = workspace.get(execution.object_id)
identifiers = workspace.identifiers()
removed = workspace.remove(execution.object_id)
```

`ExecutionWorkspace` is process-local and runtime-only. It stores `UniversalExecution` references and
supports exact identifier operations only.
