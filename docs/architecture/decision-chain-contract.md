# Decision Chain Contract

## Purpose

The Decision Chain Contract is the GAR-SPRINT-0007 Mission Echo contract for descriptive Decision
chain records.

It introduces immutable, deterministic chain models only. It does not execute chains, resolve
references, orchestrate decisions, compute outcomes, optimize choices, plan, persist records, search
records or perform AI behavior.

## Package Structure

The implementation lives in `packages/decision/chain.py` and is exported from
`packages/decision/__init__.py`.

The module defines:

- `DecisionChainType`
- `DecisionChainMetadata`
- `DecisionStepReference`
- `DecisionChain`
- `DecisionChainContract`
- `validate_decision_chain_metadata`
- `validate_decision_step_reference`
- `validate_decision_chain`
- `validate_decision_chain_contract`

## Step Reference Model

`DecisionStepReference` is an immutable opaque reference. It stores:

- decision identifier
- deterministic metadata

It never embeds a `UniversalDecision` object and never resolves the identifier.

## Chain Model

`DecisionChain` is an immutable descriptive value model. It stores:

- chain type
- ordered `DecisionStepReference` values
- deterministic metadata

It represents relationships only. It never executes or orchestrates.

## Contract Model

`DecisionChainContract` is an immutable descriptive contract. It stores:

- one or more `DecisionChain` objects
- deterministic metadata
- contract version

The contract records intended chain structure only. It has no execution or orchestration behavior.

## Validation Model

Mission Echo reuses Platform Core `ValidationResult` and `ValidationCategory` through local
validation helpers.

Validation checks:

- chain type
- chain metadata
- step reference identifier
- step reference metadata
- chain structure
- contract version
- contract chain collection
- contract metadata

No validation engine is introduced.

## Serialization Model

Chain models provide deterministic `to_dict()` payloads. Metadata dictionaries are sorted during
model construction and returned in deterministic order.

Platform Core `ObjectSerializer` remains unchanged. No Decision serializer is introduced.

## Dependency Boundaries

The Decision Chain Contract depends on Platform Core validation primitives only. It does not modify
Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning Foundation or
existing Decision Foundation behavior.

## Explicit Exclusions

The Decision Chain Contract does not implement:

- Chain execution
- Reference resolution
- Decision execution
- Orchestration
- Outcome computation
- Optimization
- Planning
- Workflow behavior
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
