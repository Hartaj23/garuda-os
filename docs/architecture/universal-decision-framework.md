# Universal Decision Framework

## Purpose

The Universal Decision Framework is the GAR-SPRINT-0007 Mission Alpha foundation for platform-level
Decision records.

It introduces deterministic, service-independent Decision models only. It does not execute
decisions, evaluate decisions, compute outcomes, optimize choices, plan, orchestrate workflow,
persist records, search records or perform AI behavior.

## Package Structure

The implementation lives under `packages/decision`:

- `__init__.py`: public Decision Foundation exports
- `core.py`: Universal Decision object, primitive enums, value models and validation helper

## Public Interfaces

Mission Alpha provides:

- `UniversalDecision`
- `DecisionType`
- `DecisionState`
- `DecisionOutcome`
- `DecisionConfidence`
- `DecisionMetadata`
- `validate_decision`

`UniversalDecision` inherits from Platform Core `CanonicalObject` and preserves Platform Core
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationships and
serialization compatibility.

## Validation Model

The framework reuses Platform Core validation and adds a local validation hook for Decision-specific
fields.

Validation checks:

- decision type
- decision state
- decision outcome
- decision confidence
- decision metadata

No validation engine is introduced.

## Serialization Model

`UniversalDecision.to_dict()` provides deterministic Decision payloads. Payloads include inherited
Platform Core fields followed by Decision-specific fields.

Platform Core `ObjectSerializer` remains unchanged and serializes inherited Platform Core fields.
No Decision serializer is introduced.

## Dependency Boundaries

The Decision Foundation depends on Platform Core. It does not modify Platform Core, Memory
Foundation, Knowledge Foundation, Context Foundation or Reasoning Foundation.

Existing foundations do not depend on Decision Foundation.

## Constitutional Rules

- Decision records remain descriptive.
- Outcomes are recorded, not computed.
- Confidence records certainty, not truth.
- Metadata is deterministic and does not influence runtime behavior.
- Platform Core remains the source of object identity and validation contracts.

## Explicit Exclusions

The Universal Decision Framework does not implement:

- Decision engine behavior
- Decision execution
- Autonomous decision making
- Outcome computation
- Decision evaluation
- Planning
- Workflow behavior
- Orchestration
- Optimization
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
