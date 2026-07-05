# Decision Strategy Contract

## Purpose

The Decision Strategy Contract is the GAR-SPRINT-0007 Mission Delta contract for descriptive
Decision strategy records.

It introduces immutable, deterministic strategy models only. It does not execute strategies,
evaluate strategies, compute decisions, optimize outcomes, plan, orchestrate workflow, persist
records, search records or perform AI behavior.

## Package Structure

The implementation lives in `packages/decision/strategy.py` and is exported from
`packages/decision/__init__.py`.

The module defines:

- `DecisionStrategyType`
- `DecisionStrategyMetadata`
- `DecisionStrategy`
- `DecisionStrategyContract`
- `validate_decision_strategy_metadata`
- `validate_decision_strategy`
- `validate_decision_strategy_contract`

## Strategy Model

`DecisionStrategy` is an immutable descriptive value model. It stores:

- strategy type
- name
- optional description
- deterministic metadata

It never executes or evaluates a strategy.

## Contract Model

`DecisionStrategyContract` is an immutable descriptive contract. It stores:

- one or more `DecisionStrategy` objects
- deterministic metadata
- contract version

The contract records intended strategy structure only. It has no execution behavior.

## Validation Model

Mission Delta reuses Platform Core `ValidationResult` and `ValidationCategory` through local
validation helpers.

Validation checks:

- strategy type
- strategy name
- strategy description
- strategy metadata
- contract version
- contract strategy collection
- contract metadata

No validation engine is introduced.

## Serialization Model

Strategy models provide deterministic `to_dict()` payloads. Metadata dictionaries are sorted during
model construction and returned in deterministic order.

Platform Core `ObjectSerializer` remains unchanged. No Decision serializer is introduced.

## Dependency Boundaries

The Decision Strategy Contract depends on Platform Core validation primitives only. It does not
modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning
Foundation or existing Decision Foundation behavior.

## Explicit Exclusions

The Decision Strategy Contract does not implement:

- Strategy execution
- Strategy evaluation
- Decision engine behavior
- Decision execution
- Outcome computation
- Optimization
- Planning
- Workflow behavior
- Orchestration
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
