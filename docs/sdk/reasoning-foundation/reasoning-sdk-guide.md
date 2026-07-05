# Reasoning Foundation SDK Guide

## Overview

The Reasoning Foundation SDK provides platform-level objects and descriptive contracts for recording
reasoning structures in Garuda. It is implemented in `packages.reasoning` and depends on Platform
Core for identity, lifecycle, validation, relationships, and serialization compatibility.

The SDK is descriptive only. It records reasoning objects, inputs, provenance, strategy contracts,
chain contracts, and runtime workspace references. It does not execute reasoning.

## Import Path

```python
from packages.reasoning import ReasoningType, UniversalReasoning
```

All public Reasoning Foundation interfaces are exported from `packages.reasoning`.

## Core Object

Use `UniversalReasoning` for platform-level Reasoning records.

```python
from packages.reasoning import ReasoningType, UniversalReasoning

reasoning = UniversalReasoning(
    reasoning_type=ReasoningType.DEDUCTIVE,
)
```

`UniversalReasoning` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Inputs And Provenance

Reasoning inputs and provenance record where descriptive Reasoning records came from.

```python
from packages.reasoning import (
    ReasoningInputCollection,
    ReasoningInputReference,
    ReasoningInputType,
    ReasoningOrigin,
    ReasoningProvenance,
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
```

Identifiers are opaque. The SDK does not resolve them.

## Strategy And Chain Contracts

Strategy and chain contracts describe supported intent and structure.

```python
from packages.reasoning import (
    ChainType,
    ReasoningChainContract,
    ReasoningStrategyContract,
    StrategyType,
)

strategy_contract = ReasoningStrategyContract(
    supported_strategy_types=(StrategyType.SEQUENTIAL,),
)
chain_contract = ReasoningChainContract(
    supported_chain_types=(ChainType.LINEAR,),
)
```

Contracts are not engines. They do not execute strategies or chains.

## Runtime Workspace

`ReasoningWorkspace` stores `UniversalReasoning` references in the current process.

```python
from packages.reasoning import ReasoningWorkspace

workspace = ReasoningWorkspace()
workspace.add(reasoning)

assert workspace.get(reasoning.object_id) is reasoning
```

The workspace is runtime-only and exact-identifier-only. It is not serializable.

## Validation

```python
result = reasoning.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and local Reasoning validation helpers. No
Reasoning-specific validation engine is implemented.

## Serialization

```python
payload = reasoning.to_dict()

assert payload["object_type"] == "UniversalReasoning"
```

`UniversalReasoning.to_dict()` provides deterministic Reasoning payloads.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(reasoning)

assert core_payload["object_id"] == str(reasoning.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalReasoning.to_dict()`.
