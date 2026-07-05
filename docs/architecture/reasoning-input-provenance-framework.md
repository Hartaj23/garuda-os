# Reasoning Input and Provenance Framework

## Scope

This document describes GAR-SPRINT-0006 Mission Bravo: the Reasoning Input and Provenance
Framework.

Mission Bravo defines immutable, descriptive models for reasoning inputs and reasoning provenance.
It does not execute reasoning, resolve references, evaluate provenance, perform inference or
generate conclusions.

## Package structure

The implementation lives in:

- `packages/reasoning/input.py`
- `packages/reasoning/provenance.py`
- `packages/reasoning/core.py` for optional `UniversalReasoning` integration
- `packages/reasoning/__init__.py` for public exports

## Public interfaces

- `ReasoningInputType`
- `ReasoningInputReference`
- `ReasoningInputCollection`
- `ReasoningOrigin`
- `ReasoningProvenance`
- `validate_reasoning_input_reference`
- `validate_reasoning_input_collection`
- `validate_reasoning_provenance`

## Input model

`ReasoningInputType` identifies the descriptive kind of input: memory, knowledge, context or
reasoning.

`ReasoningInputReference` records an opaque identifier, input type and deterministic metadata.
References do not resolve platform objects or external records.

`ReasoningInputCollection` stores immutable tuples of `ReasoningInputReference` values only. It
does not embed `UniversalMemory`, `UniversalKnowledge`, `UniversalContext` or `UniversalReasoning`
instances.

## Provenance model

`ReasoningOrigin` records descriptive origin. `ReasoningProvenance` records origin, creator,
timestamp, input references and deterministic provenance metadata.

Provenance is recorded only. It is not evaluated or interpreted.

## UniversalReasoning integration

Mission Bravo adds optional `reasoning_inputs` and `reasoning_provenance` fields to
`UniversalReasoning`.

Mission Alpha constructor compatibility is preserved. Reasoning objects created without Bravo
fields retain the Mission Alpha payload shape. When inputs or provenance are provided, their
payload fields are appended after the Mission Alpha fields.

## Validation model

Mission Bravo reuses Platform Core validation hooks and returns Platform Core `ValidationResult`
instances. Local helpers validate input type, input reference structure, provenance origin,
provenance timestamp and metadata structure.

No validation engine is introduced.

## Serialization compatibility

All Bravo value models expose deterministic `to_dict()` payloads. `UniversalReasoning.to_dict()`
remains deterministic and appends optional Bravo fields after Alpha fields.

Mission Bravo does not modify `ObjectSerializer` and does not introduce a Reasoning serializer.

## Dependency boundaries

Reasoning input references are opaque identifiers. Mission Bravo does not modify Platform Core,
Memory Foundation, Knowledge Foundation or Context Foundation packages.

## Explicitly out of scope

- Reasoning execution
- Inference
- Conclusion generation
- Reference resolution
- Provenance evaluation
- Planning
- Decision making
- Search
- Persistence
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
