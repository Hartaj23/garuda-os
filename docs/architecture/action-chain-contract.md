# Action Chain Contract

## Purpose

The Action Chain Contract is the GAR-SPRINT-0008 Mission Echo descriptive chain layer for the
Universal Action Foundation.

It records Action chain models and contract metadata only. It does not execute chains, resolve step
references, execute actions, schedule execution, orchestrate workflows, optimize behavior, persist
records, search or perform autonomous behavior.

## Package Structure

The implementation lives in `packages/action/chain.py` and is exported from
`packages/action/__init__.py`.

The module defines:

- `ActionChainType`
- `ActionChainMetadata`
- `ActionStepReference`
- `ActionChain`
- `ActionChainContract`
- `validate_action_chain_metadata`
- `validate_action_step_reference`
- `validate_action_chain`
- `validate_action_chain_contract`

## Step Reference Model

`ActionStepReference` is an immutable opaque reference. It records only:

- action identifier
- optional descriptive metadata

It never embeds `UniversalAction` instances and never resolves references.

## Chain Model

`ActionChain` is an immutable descriptive value model. It records chain type, opaque step
references and deterministic metadata.

`ActionChain` never executes and never evaluates action quality.

## Contract Model

`ActionChainContract` is an immutable contract containing `ActionChain` objects, contract metadata
and a contract version. It serializes deterministically through `to_dict()`.

The contract references Action chain objects only. It does not reference live Action objects and
does not create runtime behavior.

## Validation

Mission Echo reuses Platform Core validation primitives through `ValidationResult` and
`ValidationCategory`.

Local validation helpers verify:

- chain type
- chain metadata
- step reference structure
- chain structure
- contract structure

No validation engine is introduced.

## Serialization

All Mission Echo models provide deterministic `to_dict()` payloads. No Action serializer is
introduced and `ObjectSerializer` remains unchanged.

## Dependency Boundaries

Mission Echo depends only on Platform Core validation primitives. It does not modify Platform Core,
Memory Foundation, Knowledge Foundation, Context Foundation, Reasoning Foundation or Decision
Foundation.

## Explicit Exclusions

The Action Chain Contract does not implement:

- Chain execution
- Reference resolution
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
