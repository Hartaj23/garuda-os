# Context Selection Contract

## Scope

This document describes GAR-SPRINT-0005 Mission Echo: the Context Selection Contract.

Mission Echo defines immutable, descriptive contracts for representing Context selection intent. It
does not select contexts, resolve criteria, filter candidates, rank candidates, retrieve contexts,
search contexts or execute selection behavior.

## Package structure

The implementation lives in `packages/context/selection.py` and is exported through
`packages/context/__init__.py`.

## Public interfaces

- `SelectionType`
- `SelectionCriterion`
- `SelectionMetadata`
- `ContextSelectionRequest`
- `ContextSelectionContract`
- `validate_selection_metadata`
- `validate_selection_criterion`
- `validate_context_selection_request`
- `validate_context_selection_contract`

## Selection contract

`SelectionType` is a platform-neutral enum describing selection intent. `SelectionCriterion`
records a criterion name, operator and opaque criterion value. `ContextSelectionRequest` combines
selection type, criteria and metadata into an immutable intent payload.

`ContextSelectionContract` records supported selection types, supported criteria, metadata and a
contract version. It describes what future systems may support. It does not execute selection.

## Criterion model

Selection criteria remain opaque records. The contract does not interpret criterion values, validate
referenced Context existence or enforce criterion semantics.

## Validation model

Mission Echo provides local validation helpers that return Platform Core `ValidationResult`
instances. The helpers validate structure only: selection type, criterion shape, metadata shape and
contract shape.

No validation engine is introduced.

## Serialization compatibility

Selection models expose deterministic `to_dict()` payloads. Mission Echo does not introduce a
selection serializer and does not modify `ObjectSerializer`.

## Platform interoperability

The contract remains service-independent and infrastructure-independent. Platform Core, Memory
Foundation and Knowledge Foundation packages are unchanged. Existing Context Foundation behavior
remains intact except for required public exports.

## Explicitly out of scope

- Selection execution
- Context existence validation
- Context assembly
- Search
- Retrieval
- Filtering
- Ranking
- Prioritization
- Semantic lookup
- Reasoning
- Inference
- Persistence
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
