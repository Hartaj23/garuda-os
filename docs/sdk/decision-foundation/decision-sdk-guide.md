# Decision Foundation SDK Guide

## Overview

The Decision Foundation SDK provides immutable value models and a `UniversalDecision` platform
object for recording decisions in Garuda. It is descriptive only: it records decision category,
state, outcome, confidence, metadata, inputs, provenance, strategy contracts, chain contracts, and
runtime workspace references.

## Import Path

All public Decision Foundation interfaces are exported from `packages.decision`.

```python
from packages.decision import DecisionType, DecisionWorkspace, UniversalDecision
```

## Core Object

`UniversalDecision` inherits Platform Core `CanonicalObject` behavior. It keeps Platform Core
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

```python
from packages.decision import DecisionType, UniversalDecision

decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
)
```

## Descriptive Inputs And Provenance

Decision inputs are opaque references. Provenance records how the decision entered the platform.
Neither model resolves references or evaluates provenance.

```python
from packages.decision import (
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
)

inputs = DecisionInputCollection(
    references=(
        DecisionInputReference(
            input_type=DecisionInputType.KNOWLEDGE,
            identifier="knowledge:00000000-0000-0000-0000-000000000001",
        ),
    ),
)
provenance = DecisionProvenance(
    origin=DecisionOrigin.HUMAN,
    input_references=inputs.references,
)
```

## Contracts

Decision strategy and chain contracts are descriptive records. They do not execute strategies,
execute chains, compute outcomes, optimize decisions, or orchestrate workflow.

```python
from packages.decision import (
    DecisionChain,
    DecisionChainContract,
    DecisionChainType,
    DecisionStrategy,
    DecisionStrategyContract,
    DecisionStrategyType,
)

strategy = DecisionStrategy(
    strategy_type=DecisionStrategyType.ANALYTICAL,
    name="evidence-review",
)
strategy_contract = DecisionStrategyContract(strategies=(strategy,))

chain = DecisionChain(chain_type=DecisionChainType.SEQUENTIAL)
chain_contract = DecisionChainContract(chains=(chain,))
```

## Workspace

`DecisionWorkspace` is a process-local runtime container for `UniversalDecision` references. It
supports exact identifier operations only.

```python
from packages.decision import DecisionWorkspace

workspace = DecisionWorkspace()
workspace.add(decision)

same_decision = workspace.get(decision.object_id)
```

## Serialization And Validation

`UniversalDecision.to_dict()` provides deterministic Decision payloads. `ObjectSerializer` remains
the Platform Core serializer for inherited fields.

```python
from packages.objects import ObjectSerializer

decision_payload = decision.to_dict()
core_payload = ObjectSerializer.serialize(decision)

assert decision_payload["decision_type"] == "recommendation"
assert core_payload["object_type"] == "UniversalDecision"
```
