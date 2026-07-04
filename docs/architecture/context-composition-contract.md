# Context Composition Contract

## Scope

This document describes GAR-SPRINT-0005 Mission Delta: the Context Composition Contract.

Mission Delta defines immutable, descriptive contracts for representing how Context identifiers may
be grouped for future composition-aware systems. It does not compose contexts, resolve context
identifiers, search contexts, retrieve contexts, rank contexts or persist composed views.

## Package structure

The implementation lives in `packages/context/composition.py` and is exported through
`packages/context/__init__.py`.

## Public interfaces

- `CompositionType`
- `CompositionMetadata`
- `ContextComposition`
- `ContextCompositionContract`
- `validate_composition_metadata`
- `validate_context_composition`
- `validate_context_composition_contract`

## Composition contract

`CompositionType` is a platform-neutral enum describing composition intent. `ContextComposition`
records one composition type, opaque context identifiers and deterministic composition metadata.

`ContextCompositionContract` records supported composition types, supported metadata and a contract
version. It describes what future systems may support. It does not assemble or resolve contexts.

## Identifier model

Context identifiers remain opaque strings. The contract does not embed `UniversalContext`
instances, validate referenced Context existence or interpret identifier contents.

## Validation model

Mission Delta provides local validation helpers that return Platform Core `ValidationResult`
instances. The helpers validate structure only: composition type, identifier shape and metadata
shape.

No validation engine is introduced.

## Serialization compatibility

Composition models expose deterministic `to_dict()` payloads. Mission Delta does not introduce a
composition serializer and does not modify `ObjectSerializer`.

## Constitutional boundaries

The contract remains service-independent and infrastructure-independent. Platform Core, Memory
Foundation and Knowledge Foundation packages are unchanged. Existing Context Foundation behavior
remains intact except for required public exports.

## Explicitly out of scope

- Context composition execution
- Context resolution
- Search
- Retrieval
- Filtering
- Ranking
- Semantic lookup
- Reasoning
- Inference
- Persistence
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
