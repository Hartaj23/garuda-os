# Execution Foundation SDK Practical Examples

## Create Execution

```python
from packages.execution import ExecutionType, UniversalExecution

execution = UniversalExecution(
    execution_type=ExecutionType.ACTION,
)
```

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

## Validate Execution

```python
result = execution.validate()

assert result.is_valid
```

## Serialize Execution

```python
payload = execution.to_dict()

assert payload["object_type"] == "UniversalExecution"
assert payload["execution_type"] == "action"
assert payload["execution_inputs"]["references"][0]["input_type"] == "action"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(execution)

assert core_payload["object_type"] == "UniversalExecution"
assert core_payload["object_id"] == str(execution.object_id)
```

## Use Strategy Contracts

```python
from packages.execution import ExecutionStrategy, ExecutionStrategyContract, ExecutionStrategyType

strategy = ExecutionStrategy(
    strategy_type=ExecutionStrategyType.MANUAL,
    name="operator-review",
)
contract = ExecutionStrategyContract(strategies=(strategy,))

assert contract.to_dict()["strategies"][0]["strategy_type"] == "manual"
```

## Use Chain Contracts

```python
from packages.execution import (
    ExecutionChain,
    ExecutionChainContract,
    ExecutionChainType,
    ExecutionStepReference,
)

chain = ExecutionChain(
    chain_type=ExecutionChainType.SEQUENTIAL,
    steps=(
        ExecutionStepReference(
            execution_identifier="execution:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
contract = ExecutionChainContract(chains=(chain,))

assert contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert contract.to_dict()["chains"][0]["steps"][0]["execution_identifier"].startswith("execution:")
```

## Use The Execution Workspace

```python
from packages.execution import ExecutionWorkspace

workspace = ExecutionWorkspace()
workspace.add(execution)

assert workspace.get(execution.object_id) is execution
assert workspace.identifiers() == (execution.object_id,)
assert workspace.statistics().total_executions == 1

removed = workspace.remove(execution.object_id)

assert removed is execution
```

## Certified End-To-End Execution Flow

```python
from packages.execution import (
    ExecutionChain,
    ExecutionChainContract,
    ExecutionChainType,
    ExecutionInputCollection,
    ExecutionInputReference,
    ExecutionInputType,
    ExecutionOrigin,
    ExecutionProvenance,
    ExecutionStrategy,
    ExecutionStrategyContract,
    ExecutionStrategyType,
    ExecutionType,
    ExecutionWorkspace,
    UniversalExecution,
)
from packages.objects import ObjectSerializer

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

validation = execution.validate()
execution_payload = execution.to_dict()
core_payload = ObjectSerializer.serialize(execution)

strategy = ExecutionStrategy(
    strategy_type=ExecutionStrategyType.MANUAL,
    name="operator-review",
)
strategy_contract = ExecutionStrategyContract(strategies=(strategy,))
chain = ExecutionChain(chain_type=ExecutionChainType.SEQUENTIAL)
chain_contract = ExecutionChainContract(chains=(chain,))

workspace = ExecutionWorkspace()
workspace.add(execution)
stored_execution = workspace.get(execution.object_id)
removed_execution = workspace.remove(execution.object_id)

assert validation.is_valid
assert execution_payload["object_type"] == "UniversalExecution"
assert core_payload["object_id"] == str(execution.object_id)
assert strategy_contract.to_dict()["strategies"][0]["strategy_type"] == "manual"
assert chain_contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert stored_execution is execution
assert removed_execution is execution
assert workspace.identifiers() == ()
```

This flow mirrors the certified Execution Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine, execution
engine, strategy execution, chain execution, outcome computation, reference resolution, provenance
evaluation, scheduling, orchestration, optimization, workflow, AI, frontend, autonomous behavior,
Agent, trading, or portfolio functionality.
