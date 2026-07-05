# Universal Action Framework

## Purpose

The Universal Action Framework is the GAR-SPRINT-0008 Mission Alpha foundation for descriptive
Action objects.

It introduces `UniversalAction` and Action-specific primitives under `packages/action`. Action
objects record action category, lifecycle state, outcome category, confidence and metadata. They do
not execute actions, schedule execution, orchestrate workflows, evaluate outcomes, optimize
behavior, persist records, search or perform autonomous behavior.

## Package Structure

The implementation lives in:

- `packages/action/__init__.py`
- `packages/action/core.py`

The public package exports:

- `UniversalAction`
- `ActionType`
- `ActionState`
- `ActionOutcome`
- `ActionConfidence`
- `ActionMetadata`
- `validate_action`

## Platform Core Integration

`UniversalAction` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage and
serialization compatibility for inherited fields.

Mission Alpha does not modify Platform Core or `ObjectSerializer`.

## Action Models

`ActionType`, `ActionState` and `ActionOutcome` are platform-neutral enumerations. They classify
Action records only.

`ActionConfidence` and `ActionMetadata` are immutable value models with deterministic `to_dict()`
payloads. Metadata may record descriptive fields such as author, version or description, but it
does not influence runtime behavior.

## Serialization

`UniversalAction.to_dict()` returns a deterministic payload containing inherited Platform Core
fields followed by Action-specific fields:

- `action_type`
- `action_state`
- `action_outcome`
- `action_confidence`
- `action_metadata`

Platform Core `ObjectSerializer` remains the serializer for inherited object fields.

## Validation

Mission Alpha reuses Platform Core validation through the existing validation hook path.
`validate_action` checks:

- Action type
- Action state
- Action outcome
- Action confidence
- Action metadata

No validation engine is introduced.

## Dependency Boundaries

The Action Foundation depends only on Platform Core. Mission Alpha does not modify Memory
Foundation, Knowledge Foundation, Context Foundation, Reasoning Foundation or Decision Foundation.

## Explicit Exclusions

The Universal Action Framework does not implement:

- Action execution
- Workflow engines
- Orchestration
- Scheduling
- Outcome evaluation
- Optimization
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
