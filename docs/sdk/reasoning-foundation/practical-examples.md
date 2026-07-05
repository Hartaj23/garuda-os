# Reasoning Foundation SDK Practical Examples

## Create Reasoning

```python
from packages.reasoning import ReasoningType, UniversalReasoning

reasoning = UniversalReasoning(
    reasoning_type=ReasoningType.DEDUCTIVE,
)
```

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

## Validate Reasoning

```python
result = reasoning.validate()

assert result.is_valid
```

## Serialize Reasoning

```python
payload = reasoning.to_dict()

assert payload["object_type"] == "UniversalReasoning"
assert payload["reasoning_type"] == "deductive"
assert payload["reasoning_inputs"]["references"][0]["input_type"] == "knowledge"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(reasoning)

assert core_payload["object_type"] == "UniversalReasoning"
assert core_payload["object_id"] == str(reasoning.object_id)
```

## Use Strategy Contracts

```python
from packages.reasoning import ReasoningStrategy, StrategyType

strategy = ReasoningStrategy(
    strategy_type=StrategyType.SEQUENTIAL,
    name="ordered-review",
)

strategy_payload = strategy.to_dict()

assert strategy_payload["strategy_type"] == "sequential"
```

## Use Chain Contracts

```python
from packages.reasoning import (
    ChainType,
    ReasoningChain,
    ReasoningStepReference,
)

chain = ReasoningChain(
    chain_type=ChainType.LINEAR,
    steps=(
        ReasoningStepReference(
            identifier="reasoning-step:00000000-0000-0000-0000-000000000001",
            sequence=0,
        ),
    ),
)

chain_payload = chain.to_dict()

assert chain_payload["chain_type"] == "linear"
assert chain_payload["steps"][0]["sequence"] == 0
```

## Use The Reasoning Workspace

```python
from packages.reasoning import ReasoningWorkspace

workspace = ReasoningWorkspace()
workspace.add(reasoning)

assert workspace.get(reasoning.object_id) is reasoning
assert workspace.identifiers() == (reasoning.object_id,)

removed = workspace.remove(reasoning.object_id)

assert removed is reasoning
```

## Certified End-To-End Reasoning Flow

```python
from packages.objects import ObjectSerializer
from packages.reasoning import (
    ChainType,
    ReasoningChainContract,
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningOrigin,
    ReasoningProvenance,
    ReasoningStrategyContract,
    ReasoningType,
    ReasoningWorkspace,
    StrategyType,
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

validation = reasoning.validate()
reasoning_payload = reasoning.to_dict()
core_payload = ObjectSerializer.serialize(reasoning)

strategy_contract = ReasoningStrategyContract(
    supported_strategy_types=(StrategyType.SEQUENTIAL,),
)
chain_contract = ReasoningChainContract(
    supported_chain_types=(ChainType.LINEAR,),
)

workspace = ReasoningWorkspace()
workspace.add(reasoning)
stored_reasoning = workspace.get(reasoning.object_id)
removed_reasoning = workspace.remove(reasoning.object_id)

assert validation.is_valid
assert reasoning_payload["object_type"] == "UniversalReasoning"
assert core_payload["object_id"] == str(reasoning.object_id)
assert strategy_contract.to_dict()["supported_strategy_types"] == ["sequential"]
assert chain_contract.to_dict()["supported_chain_types"] == ["linear"]
assert stored_reasoning is reasoning
assert removed_reasoning is reasoning
assert workspace.identifiers() == ()
```

This flow mirrors the certified Reasoning Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine, reasoning
engine, strategy execution, chain execution, inference, conclusion generation, planning, decision
making, orchestration, workflow, AI, frontend, Decision, Agent, trading, or portfolio
functionality.
