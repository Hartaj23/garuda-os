# Action Foundation SDK Extension Guide

## Extension Principles

Extensions must preserve the Action Foundation boundary:

- Platform Core remains the source of object identity, lifecycle, validation primitives, and
  inherited serialization compatibility.
- Action value models remain deterministic.
- References remain opaque unless a future approved mission introduces resolution behavior.
- Contracts remain descriptive unless a future approved mission introduces execution behavior.
- `ActionWorkspace` remains runtime-only and process-local.

## Additive Documentation Extensions

Documentation may be extended to cover newly approved and implemented Action Foundation behavior.
Do not document proposed or future behavior as available.

## Additive Model Extensions

Future model additions should follow the existing pattern:

- immutable dataclasses for value models
- explicit enum values for platform-neutral categories
- deterministic `to_dict()` payloads
- local validation helpers returning Platform Core `ValidationResult`
- no custom serializer
- no validation engine

## Workspace Extensions

The implemented `ActionWorkspace` supports exact identifier operations only. Do not extend it into a
database, cache, search index, retrieval engine, scheduler, executor, orchestrator, persistence
adapter, or workflow engine without separate architecture approval.

## Cross-Foundation Extensions

Action models may record identifiers associated with Memory, Knowledge, Context, Reasoning, and
Decision foundations. These identifiers remain opaque in the implemented SDK.

Do not embed `UniversalMemory`, `UniversalKnowledge`, `UniversalContext`, `UniversalReasoning`, or
`UniversalDecision` objects in Action input references or chain step references.

## Out-Of-Scope Extensions

The following capabilities are not implemented and must not be treated as available SDK behavior:

- action execution
- strategy execution
- chain execution
- outcome computation
- reference resolution
- provenance evaluation
- scheduling
- orchestration
- optimization
- persistence
- search
- AI integration
- REST APIs
- frontend behavior
- autonomous behavior
- workflow behavior
