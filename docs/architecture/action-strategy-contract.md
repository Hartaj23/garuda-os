# Action Strategy Contract

## Purpose

The Action Strategy Contract is the GAR-SPRINT-0008 Mission Delta descriptive strategy layer for
the Universal Action Foundation.

It records Action strategy models and contract metadata only. It does not execute strategies,
evaluate strategy quality, execute actions, schedule execution, orchestrate workflows, optimize
behavior, persist records, search or perform autonomous behavior.

## Package Structure

The implementation lives in `packages/action/strategy.py` and is exported from
`packages/action/__init__.py`.

The module defines:

- `ActionStrategyType`
- `ActionStrategyMetadata`
- `ActionStrategy`
- `ActionStrategyContract`
- `validate_action_strategy_metadata`
- `validate_action_strategy`
- `validate_action_strategy_contract`

## Strategy Model

`ActionStrategy` is an immutable descriptive value model. It records:

- strategy type
- name
- optional description
- deterministic metadata

`ActionStrategy` never executes and never evaluates action quality.

## Contract Model

`ActionStrategyContract` is an immutable contract containing `ActionStrategy` objects, contract
metadata and a contract version. It serializes deterministically through `to_dict()`.

The contract references Action strategy objects only. It does not reference live Action objects and
does not create runtime behavior.

## Validation

Mission Delta reuses Platform Core validation primitives through `ValidationResult` and
`ValidationCategory`.

Local validation helpers verify:

- strategy type
- strategy metadata
- strategy structure
- contract structure

No validation engine is introduced.

## Serialization

All Mission Delta models provide deterministic `to_dict()` payloads. No Action serializer is
introduced and `ObjectSerializer` remains unchanged.

## Dependency Boundaries

Mission Delta depends only on Platform Core validation primitives. It does not modify Platform
Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning Foundation or Decision
Foundation.

## Explicit Exclusions

The Action Strategy Contract does not implement:

- Strategy execution
- Strategy evaluation
- Action execution
- Scheduling
- Workflow orchestration
- Optimization
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
