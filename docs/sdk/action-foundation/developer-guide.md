# Action Foundation Developer Guide

## Create Universal Action

```python
from packages.action import ActionType, UniversalAction

action = UniversalAction(
    action_type=ActionType.TASK,
)
```

`UniversalAction` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Use Outcome, Confidence, And Metadata

```python
from packages.action import (
    ActionConfidence,
    ActionMetadata,
    ActionOutcome,
    ActionState,
    ActionType,
    UniversalAction,
)

action = UniversalAction(
    action_type=ActionType.REVIEW,
    action_state=ActionState.READY,
    action_outcome=ActionOutcome.UNKNOWN,
    action_confidence=ActionConfidence(level="high", rationale="reviewed"),
    action_metadata=ActionMetadata(values={"domain": "platform"}),
)
```

`ActionConfidence` records confidence about the Action record. It does not compute truth, execute
an action, schedule work, or determine an outcome.

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

Inputs and provenance are descriptive. They do not resolve identifiers or evaluate provenance.

## Validate Action

```python
result = action.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Action-specific checks through the
existing validation hook path.

## Serialize Action

```python
payload = action.to_dict()

assert payload["object_type"] == "UniversalAction"
assert payload["action_type"] == "task"
```

`UniversalAction.to_dict()` is the deterministic Action payload.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(action)

assert core_payload["object_type"] == "UniversalAction"
assert core_payload["object_id"] == str(action.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalAction.to_dict()`.

## Use Strategy Contracts

```python
from packages.action import ActionStrategy, ActionStrategyType

strategy = ActionStrategy(
    strategy_type=ActionStrategyType.MANUAL,
    name="operator-review",
)
```

Strategy contracts describe strategy intent. They do not execute strategies or optimize actions.

## Use Chain Contracts

```python
from packages.action import ActionChain, ActionChainType

chain = ActionChain(
    chain_type=ActionChainType.SEQUENTIAL,
)
```

Chain contracts describe chain structure. They do not execute chains or resolve step references.

## Use The Action Workspace

```python
from packages.action import ActionWorkspace

workspace = ActionWorkspace()
workspace.add(action)

same_action = workspace.get(action.object_id)
identifiers = workspace.identifiers()
removed = workspace.remove(action.object_id)
```

`ActionWorkspace` is process-local and runtime-only. It stores `UniversalAction` references and
supports exact identifier operations only.
