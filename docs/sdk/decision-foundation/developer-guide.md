# Decision Foundation Developer Guide

## Create Universal Decision

```python
from packages.decision import DecisionType, UniversalDecision

decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
)
```

`UniversalDecision` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Use Outcome, Confidence, And Metadata

```python
from packages.decision import (
    DecisionConfidence,
    DecisionMetadata,
    DecisionOutcome,
    DecisionState,
    DecisionType,
    UniversalDecision,
)

decision = UniversalDecision(
    decision_type=DecisionType.SELECTION,
    decision_state=DecisionState.CONFIRMED,
    decision_outcome=DecisionOutcome.ACCEPTED,
    decision_confidence=DecisionConfidence(level="high", rationale="reviewed"),
    decision_metadata=DecisionMetadata(values={"domain": "platform"}),
)
```

`DecisionConfidence` records confidence about the Decision record. It does not compute truth,
execute a decision, or determine an outcome.

## Add Inputs And Provenance

```python
from packages.decision import (
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
    DecisionType,
    UniversalDecision,
)

inputs = DecisionInputCollection(
    references=(
        DecisionInputReference(
            input_type=DecisionInputType.REASONING,
            identifier="reasoning:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = DecisionProvenance(
    origin=DecisionOrigin.HUMAN,
    input_references=inputs.references,
)
decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
    decision_inputs=inputs,
    decision_provenance=provenance,
)
```

Inputs and provenance are descriptive. They do not resolve identifiers or evaluate provenance.

## Validate Decision

```python
result = decision.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Decision-specific checks through the
existing validation hook path.

## Serialize Decision

```python
payload = decision.to_dict()

assert payload["object_type"] == "UniversalDecision"
assert payload["decision_type"] == "recommendation"
```

`UniversalDecision.to_dict()` is the deterministic Decision payload.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(decision)

assert core_payload["object_type"] == "UniversalDecision"
assert core_payload["object_id"] == str(decision.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalDecision.to_dict()`.

## Use Strategy Contracts

```python
from packages.decision import DecisionStrategy, DecisionStrategyType

strategy = DecisionStrategy(
    strategy_type=DecisionStrategyType.ANALYTICAL,
    name="evidence-review",
)
```

Strategy contracts describe strategy intent. They do not execute strategies or optimize decisions.

## Use Chain Contracts

```python
from packages.decision import DecisionChain, DecisionChainType

chain = DecisionChain(
    chain_type=DecisionChainType.SEQUENTIAL,
)
```

Chain contracts describe chain structure. They do not execute chains or resolve step references.

## Use The Decision Workspace

```python
from packages.decision import DecisionWorkspace

workspace = DecisionWorkspace()
workspace.add(decision)

same_decision = workspace.get(decision.object_id)
identifiers = workspace.identifiers()
removed = workspace.remove(decision.object_id)
```

`DecisionWorkspace` is process-local and runtime-only. It stores `UniversalDecision` references and
supports exact identifier operations only.
