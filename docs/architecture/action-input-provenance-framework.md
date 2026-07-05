# Action Input and Provenance Framework

## Purpose

The Action Input and Provenance Framework is the GAR-SPRINT-0008 Mission Bravo extension to the
Universal Action Foundation.

It introduces immutable, deterministic and descriptive input and provenance models for Action
records. It does not resolve references, evaluate provenance, execute actions, schedule execution,
orchestrate workflows, optimize behavior, persist records, search or perform autonomous behavior.

## Package Structure

The implementation lives in:

- `packages/action/input.py`
- `packages/action/provenance.py`
- optional integration in `packages/action/core.py`
- public exports in `packages/action/__init__.py`

The module set defines:

- `ActionInputType`
- `ActionInputReference`
- `ActionInputCollection`
- `ActionOrigin`
- `ActionProvenance`
- local validation helpers

## Input Model

`ActionInputReference` is an immutable opaque reference. It records:

- input type
- identifier
- optional descriptive metadata

`ActionInputCollection` stores immutable tuples of input references and emits deterministic
payloads. References remain opaque and are never resolved by Mission Bravo.

## Provenance Model

`ActionProvenance` records descriptive Action origin, source identifier, timestamp, input
references and metadata. Provenance is recorded only. It does not verify, evaluate or influence
runtime behavior.

## UniversalAction Integration

`UniversalAction` accepts optional `action_inputs` and `action_provenance` arguments. Mission Alpha
constructor compatibility is preserved. When present, Bravo fields are appended after the Mission
Alpha payload fields:

- `action_inputs`
- `action_provenance`

## Validation

Mission Bravo reuses Platform Core validation primitives through `ValidationResult` and
`ValidationCategory`.

Local validation helpers verify:

- input reference shape
- input collection structure
- provenance record structure

No validation engine is introduced.

## Dependency Boundaries

Action input references may contain opaque identifiers for Memory, Knowledge, Context, Reasoning,
Decision or external records. They do not embed live objects from those foundations.

Mission Bravo does not modify Platform Core, Memory Foundation, Knowledge Foundation, Context
Foundation, Reasoning Foundation or Decision Foundation.

## Explicit Exclusions

The Action Input and Provenance Framework does not implement:

- Reference resolution
- Provenance evaluation
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
