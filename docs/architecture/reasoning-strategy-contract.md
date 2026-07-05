# Reasoning Strategy Contract

## Scope

This document describes GAR-SPRINT-0006 Mission Delta: the Reasoning Strategy Contract.

Mission Delta defines immutable, descriptive models for recording strategy intent. It does not
execute strategies, execute reasoning, perform inference, generate conclusions, plan decisions,
search, persist records or perform AI behavior.

## Package structure

The implementation lives in `packages/reasoning/strategy.py` and is exported through
`packages/reasoning/__init__.py`.

## Public interfaces

- `StrategyType`
- `StrategyMetadata`
- `ReasoningStrategy`
- `ReasoningStrategyContract`
- `validate_strategy_metadata`
- `validate_reasoning_strategy`
- `validate_reasoning_strategy_contract`

## Strategy contract

`StrategyType` records the descriptive category of the strategy. `StrategyMetadata` stores
deterministic metadata. `ReasoningStrategy` records a type, name, description and metadata.
`ReasoningStrategyContract` records supported strategy types, metadata and contract version.

These models are descriptive only. They contain no executable behavior and do not influence
reasoning execution.

## Validation model

Mission Delta provides local validation helpers that return Platform Core `ValidationResult`
instances. The helpers validate strategy type, strategy name, optional description, strategy
metadata and contract structure.

No validation engine is introduced.

## Serialization compatibility

Strategy models expose deterministic `to_dict()` payloads. Mission Delta does not modify
`ObjectSerializer` and does not introduce a strategy serializer.

## Dependency boundaries

Reasoning Strategy Contract depends only on Platform Core validation result types. Mission Delta
does not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
existing Reasoning Foundation behavior beyond required public exports.

## Explicitly out of scope

- Reasoning engine behavior
- Strategy execution
- Reasoning execution
- Inference
- Conclusion generation
- Planning
- Decision making
- Search
- Persistence
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
