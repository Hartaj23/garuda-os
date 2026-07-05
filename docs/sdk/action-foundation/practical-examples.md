# Action Foundation SDK Practical Examples

## Create Action

```python
from packages.action import ActionType, UniversalAction

action = UniversalAction(
    action_type=ActionType.TASK,
)
```

## Add Inputs And Provenance

```python
from packages.action import (
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionOrigin,
    ActionProvenance,
    ActionType,
    UniversalAction,
)

inputs = ActionInputCollection(
    references=(
        ActionInputReference(
            input_type=ActionInputType.DECISION,
            identifier="decision:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = ActionProvenance(
    origin=ActionOrigin.DECISION,
    input_references=inputs.references,
)
action = UniversalAction(
    action_type=ActionType.TASK,
    action_inputs=inputs,
    action_provenance=provenance,
)
```

## Validate Action

```python
result = action.validate()

assert result.is_valid
```

## Serialize Action

```python
payload = action.to_dict()

assert payload["object_type"] == "UniversalAction"
assert payload["action_type"] == "task"
assert payload["action_inputs"]["references"][0]["input_type"] == "decision"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(action)

assert core_payload["object_type"] == "UniversalAction"
assert core_payload["object_id"] == str(action.object_id)
```

## Use Strategy Contracts

```python
from packages.action import ActionStrategy, ActionStrategyContract, ActionStrategyType

strategy = ActionStrategy(
    strategy_type=ActionStrategyType.MANUAL,
    name="operator-review",
)
contract = ActionStrategyContract(strategies=(strategy,))

assert contract.to_dict()["strategies"][0]["strategy_type"] == "manual"
```

## Use Chain Contracts

```python
from packages.action import (
    ActionChain,
    ActionChainContract,
    ActionChainType,
    ActionStepReference,
)

chain = ActionChain(
    chain_type=ActionChainType.SEQUENTIAL,
    steps=(
        ActionStepReference(
            action_identifier="action:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
contract = ActionChainContract(chains=(chain,))

assert contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert contract.to_dict()["chains"][0]["steps"][0]["action_identifier"].startswith("action:")
```

## Use The Action Workspace

```python
from packages.action import ActionWorkspace

workspace = ActionWorkspace()
workspace.add(action)

assert workspace.get(action.object_id) is action
assert workspace.identifiers() == (action.object_id,)
assert workspace.statistics().total_actions == 1

removed = workspace.remove(action.object_id)

assert removed is action
```

## Certified End-To-End Action Flow

```python
from packages.action import (
    ActionChain,
    ActionChainContract,
    ActionChainType,
    ActionInputCollection,
    ActionInputReference,
    ActionInputType,
    ActionOrigin,
    ActionProvenance,
    ActionStrategy,
    ActionStrategyContract,
    ActionStrategyType,
    ActionType,
    ActionWorkspace,
    UniversalAction,
)
from packages.objects import ObjectSerializer

inputs = ActionInputCollection(
    references=(
        ActionInputReference(
            input_type=ActionInputType.DECISION,
            identifier="decision:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = ActionProvenance(
    origin=ActionOrigin.DECISION,
    input_references=inputs.references,
)
action = UniversalAction(
    action_type=ActionType.TASK,
    action_inputs=inputs,
    action_provenance=provenance,
)

validation = action.validate()
action_payload = action.to_dict()
core_payload = ObjectSerializer.serialize(action)

strategy = ActionStrategy(
    strategy_type=ActionStrategyType.MANUAL,
    name="operator-review",
)
strategy_contract = ActionStrategyContract(strategies=(strategy,))
chain = ActionChain(chain_type=ActionChainType.SEQUENTIAL)
chain_contract = ActionChainContract(chains=(chain,))

workspace = ActionWorkspace()
workspace.add(action)
stored_action = workspace.get(action.object_id)
removed_action = workspace.remove(action.object_id)

assert validation.is_valid
assert action_payload["object_type"] == "UniversalAction"
assert core_payload["object_id"] == str(action.object_id)
assert strategy_contract.to_dict()["strategies"][0]["strategy_type"] == "manual"
assert chain_contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert stored_action is action
assert removed_action is action
assert workspace.identifiers() == ()
```

This flow mirrors the certified Action Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine, action
engine, strategy execution, chain execution, outcome computation, reference resolution, provenance
evaluation, scheduling, orchestration, optimization, workflow, AI, frontend, autonomous behavior,
Agent, trading, or portfolio functionality.
