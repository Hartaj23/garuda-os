# Context Source and Scope Framework

## Scope

This document describes GAR-SPRINT-0005 Mission Bravo: the Context Source and Scope Framework.

Mission Bravo adds descriptive source and scope models to the Universal Context Framework. It does
not implement context composition, context selection, retrieval, source resolution, boundary
enforcement, prioritization, reasoning, inference, persistence, search, AI behavior, REST
endpoints, frontend behavior or workflow behavior.

## Package structure

The implementation lives in:

- `packages/context/source.py`
- `packages/context/scope.py`
- `packages/context/core.py`

## Source model

`ContextSourceType` describes where context originated. `ContextSource` records source type, an
opaque source identifier, creation timestamp and deterministic metadata.

Sources do not resolve identifiers, retrieve objects, validate external existence or load
resources.

## Scope model

`ContextScopeType` describes the category of context boundary. `ContextScope` records scope type,
boundary identifier, lifetime metadata and deterministic descriptive metadata.

Scopes do not enforce boundaries and do not implement lifecycle behavior.

## Universal Context integration

`UniversalContext` accepts optional `context_source` and `context_scope` values. Mission Alpha
constructor compatibility is preserved, and new payload keys are appended after the existing
Mission Alpha context payload fields.

## Validation model

Universal Context validation continues to use the existing Platform Core validation hook path.
Mission Bravo validation checks only source type, scope type, source metadata and scope metadata
shape. It does not perform source resolution, retrieval checks or boundary enforcement.

## Serialization compatibility

`ContextSource`, `ContextScope` and `UniversalContext.to_dict()` provide deterministic payloads.
Mission Bravo does not introduce a dedicated serializer and does not modify `ObjectSerializer`.

## Dependency boundaries

Mission Bravo does not modify Platform Core, Memory Foundation or Knowledge Foundation packages.
Context source identifiers and scope boundary identifiers remain opaque strings.

## Explicitly out of scope

- Context composition
- Context selection
- Retrieval
- Source resolution
- Boundary enforcement
- Reasoning
- Inference
- Prioritization
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
