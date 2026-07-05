# Decision Foundation SDK Practical Examples

## Create Decision

```python
from packages.decision import DecisionType, UniversalDecision

decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
)
```

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

## Validate Decision

```python
result = decision.validate()

assert result.is_valid
```

## Serialize Decision

```python
payload = decision.to_dict()

assert payload["object_type"] == "UniversalDecision"
assert payload["decision_type"] == "recommendation"
assert payload["decision_inputs"]["references"][0]["input_type"] == "reasoning"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(decision)

assert core_payload["object_type"] == "UniversalDecision"
assert core_payload["object_id"] == str(decision.object_id)
```

## Use Strategy Contracts

```python
from packages.decision import DecisionStrategy, DecisionStrategyContract, DecisionStrategyType

strategy = DecisionStrategy(
    strategy_type=DecisionStrategyType.ANALYTICAL,
    name="evidence-review",
)
contract = DecisionStrategyContract(strategies=(strategy,))

assert contract.to_dict()["strategies"][0]["strategy_type"] == "analytical"
```

## Use Chain Contracts

```python
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainType,
    DecisionStepReference,
)

chain = DecisionChain(
    chain_type=DecisionChainType.SEQUENTIAL,
    steps=(
        DecisionStepReference(
            decision_identifier="decision:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
contract = DecisionChainContract(chains=(chain,))

assert contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert contract.to_dict()["chains"][0]["steps"][0]["decision_identifier"].startswith("decision:")
```

## Use The Decision Workspace

```python
from packages.decision import DecisionWorkspace

workspace = DecisionWorkspace()
workspace.add(decision)

assert workspace.get(decision.object_id) is decision
assert workspace.identifiers() == (decision.object_id,)
assert workspace.statistics().total_decisions == 1

removed = workspace.remove(decision.object_id)

assert removed is decision
```

## Certified End-To-End Decision Flow

```python
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainType,
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
    DecisionStrategy,
    DecisionStrategyContract,
    DecisionStrategyType,
    DecisionType,
    DecisionWorkspace,
    UniversalDecision,
)
from packages.objects import ObjectSerializer

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

validation = decision.validate()
decision_payload = decision.to_dict()
core_payload = ObjectSerializer.serialize(decision)

strategy = DecisionStrategy(
    strategy_type=DecisionStrategyType.ANALYTICAL,
    name="evidence-review",
)
strategy_contract = DecisionStrategyContract(strategies=(strategy,))
chain = DecisionChain(chain_type=DecisionChainType.SEQUENTIAL)
chain_contract = DecisionChainContract(chains=(chain,))

workspace = DecisionWorkspace()
workspace.add(decision)
stored_decision = workspace.get(decision.object_id)
removed_decision = workspace.remove(decision.object_id)

assert validation.is_valid
assert decision_payload["object_type"] == "UniversalDecision"
assert core_payload["object_id"] == str(decision.object_id)
assert strategy_contract.to_dict()["strategies"][0]["strategy_type"] == "analytical"
assert chain_contract.to_dict()["chains"][0]["chain_type"] == "sequential"
assert stored_decision is decision
assert removed_decision is decision
assert workspace.identifiers() == ()
```

This flow mirrors the certified Decision Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine, decision
engine, strategy execution, chain execution, outcome computation, reference resolution, provenance
evaluation, orchestration, planning, optimization, workflow, AI, frontend, autonomous behavior,
Agent, trading, or portfolio functionality.
