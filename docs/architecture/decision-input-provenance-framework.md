# Decision Input and Provenance Framework

## Purpose

The Decision Input and Provenance Framework is the GAR-SPRINT-0007 Mission Bravo extension for
descriptive Decision records.

It introduces opaque input references and provenance records only. It does not resolve references,
evaluate provenance, compute outcomes, execute decisions, optimize choices, plan, orchestrate
workflow, persist records, search records or perform AI behavior.

## Package Structure

The implementation lives under `packages/decision`:

- `input.py`: input type, opaque input reference, input collection and validation helpers
- `provenance.py`: decision origin, provenance record and validation helper
- `core.py`: optional `UniversalDecision` integration for inputs and provenance
- `__init__.py`: public Decision Foundation exports

## Public Interfaces

Mission Bravo provides:

- `DecisionInputType`
- `DecisionInputReference`
- `DecisionInputCollection`
- `DecisionOrigin`
- `DecisionProvenance`
- `validate_decision_input_reference`
- `validate_decision_input_collection`
- `validate_decision_provenance`

`UniversalDecision` accepts optional `decision_inputs` and `decision_provenance` values. Mission
Alpha constructor compatibility is preserved.

## Input Model

Decision input references are immutable value records. They store:

- input type
- opaque identifier
- deterministic metadata

They never embed Memory, Knowledge, Context, Reasoning or external objects and never resolve
identifiers.

## Provenance Model

Decision provenance records are immutable value records. They store:

- origin
- optional author
- created timestamp
- optional opaque input references
- deterministic metadata

They do not evaluate provenance quality or trust.

## Validation Model

Mission Bravo reuses Platform Core `ValidationResult` and `ValidationCategory` through local
validation helpers.

Validation checks:

- input type
- input identifier
- input reference metadata
- input collection shape
- provenance origin
- provenance author
- provenance timestamp
- provenance metadata

No validation engine is introduced.

## Serialization Model

Input and provenance models provide deterministic `to_dict()` payloads.

`UniversalDecision.to_dict()` appends optional Bravo payload fields after the existing Mission Alpha
fields:

- `decision_inputs`
- `decision_provenance`

Platform Core `ObjectSerializer` remains unchanged. No Decision serializer is introduced.

## Dependency Boundaries

Decision input references may name Memory, Knowledge, Context or Reasoning records by opaque string
identifier. The Decision Foundation does not import or embed those objects for input records.

Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation and Reasoning Foundation
remain unchanged.

## Explicit Exclusions

The Decision Input and Provenance Framework does not implement:

- Decision engine behavior
- Reference resolution
- Provenance evaluation
- Decision execution
- Outcome computation
- Planning
- Workflow behavior
- Orchestration
- Optimization
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
