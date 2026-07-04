# Universal Context Framework

## Scope

This document describes GAR-SPRINT-0005 Mission Alpha: the Universal Context Framework.

Mission Alpha establishes the canonical platform object for Context. It does not implement context
composition, context selection, prioritization, planning, reasoning, inference, persistence,
search, AI behavior, REST endpoints, frontend behavior or workflow behavior.

## Included capabilities

- `UniversalContext`
- `ContextType`
- `ContextState`
- `ContextConfidence`
- `ContextMetadata`
- Context-specific validation hook
- Deterministic `to_dict` payload support

## Object model

`UniversalContext` inherits from Platform Core `CanonicalObject`. It therefore reuses object
identity, object type, schema version, object version, metadata, tags, lifecycle state, audit
fields, behavior registration, relationship storage and validation hooks.

The framework does not introduce a second object base class and does not modify Platform Core.

## Governance state

`ContextState` describes constitutional maturity for a context object. It is separate from Platform
Core lifecycle state. Platform Core lifecycle still controls draft, active and archived object
lifecycle behavior.

## Confidence model

`ContextConfidence` records confidence in context completeness. It does not represent truth and
does not perform reasoning, inference, prioritization or selection.

## Metadata model

`ContextMetadata` stores deterministic context-specific metadata such as scope, boundaries, version
or creation information. Metadata remains descriptive and does not influence behavior.

## Validation model

Universal Context validation is implemented as an object validation hook registered by
`UniversalContext`. The hook validates only Mission Alpha context invariants and merges with the
existing Platform Core validation result.

## Serialization compatibility

`UniversalContext.to_dict()` provides deterministic context payloads. Existing Platform Core
`ObjectSerializer` remains responsible for inherited object fields only.

## Dependency boundaries

The Context package depends on Platform Core only. Mission Alpha does not modify Platform Core,
Memory Foundation or Knowledge Foundation packages.

## Explicitly out of scope

- Context composition
- Context selection
- Reasoning
- Inference
- Prioritization
- Planning
- Persistence
- Search
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
