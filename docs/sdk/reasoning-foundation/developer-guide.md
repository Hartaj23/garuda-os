# Reasoning Foundation Developer Guide

## Create Universal Reasoning

```python
from packages.reasoning import ReasoningType, UniversalReasoning

reasoning = UniversalReasoning(
    reasoning_type=ReasoningType.DEDUCTIVE,
)
```

`UniversalReasoning` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Use Confidence And Metadata

```python
from packages.reasoning import (
    ReasoningConfidence,
    ReasoningMetadata,
    ReasoningState,
    ReasoningType,
    UniversalReasoning,
)

reasoning = UniversalReasoning(
    reasoning_type=ReasoningType.COMPARATIVE,
    reasoning_state=ReasoningState.VALIDATED,
    reasoning_confidence=ReasoningConfidence(level="high", rationale="certified"),
    reasoning_metadata=ReasoningMetadata(values={"domain": "platform"}),
)
```

`ReasoningConfidence` records confidence about the Reasoning record. It does not determine truth or
execute reasoning.

## Add Inputs And Provenance

```python
from packages.reasoning import (
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningOrigin,
    ReasoningProvenance,
    ReasoningType,
    UniversalReasoning,
)

inputs = ReasoningInputCollection(
    references=(
        ReasoningInputReference(
            input_type=ReasoningInputType.KNOWLEDGE,
            identifier="knowledge:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = ReasoningProvenance(
    origin=ReasoningOrigin.HUMAN_DEFINED,
    input_references=inputs.references,
)
reasoning = UniversalReasoning(
    reasoning_type=ReasoningType.DEDUCTIVE,
    reasoning_inputs=inputs,
    reasoning_provenance=provenance,
)
```

Inputs and provenance are descriptive. They do not resolve identifiers or evaluate provenance.

## Validate Reasoning

```python
result = reasoning.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Reasoning-specific checks through the
existing validation hook path.

## Serialize Reasoning

```python
payload = reasoning.to_dict()

assert payload["object_type"] == "UniversalReasoning"
assert payload["reasoning_type"] == "deductive"
```

`UniversalReasoning.to_dict()` is the deterministic Reasoning payload.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(reasoning)

assert core_payload["object_type"] == "UniversalReasoning"
assert core_payload["object_id"] == str(reasoning.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalReasoning.to_dict()`.

## Use Strategy Contracts

```python
from packages.reasoning import ReasoningStrategy, StrategyType

strategy = ReasoningStrategy(
    strategy_type=StrategyType.SEQUENTIAL,
    name="ordered-review",
)
```

Strategy contracts describe strategy intent. They do not execute strategies.

## Use Chain Contracts

```python
from packages.reasoning import ChainType, ReasoningChain

chain = ReasoningChain(
    chain_type=ChainType.LINEAR,
)
```

Chain contracts describe chain structure. They do not execute chains or resolve step references.

## Use The Reasoning Workspace

```python
from packages.reasoning import ReasoningWorkspace

workspace = ReasoningWorkspace()
workspace.add(reasoning)

same_reasoning = workspace.get(reasoning.object_id)
identifiers = workspace.identifiers()
removed = workspace.remove(reasoning.object_id)
```

`ReasoningWorkspace` is process-local and runtime-only. It stores `UniversalReasoning` references
and supports exact identifier operations only.
