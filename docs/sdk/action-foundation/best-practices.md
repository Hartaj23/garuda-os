# Action Foundation SDK Best Practices

## Use Action Objects As Records

Use `UniversalAction` to record action state, outcome, confidence, metadata, inputs, and provenance.
Do not use it as an executor, scheduler, orchestrator, workflow engine, or autonomous agent.

## Keep References Opaque

Use `ActionInputReference.identifier` and `ActionStepReference.action_identifier` as opaque strings.
Store identifiers, not live objects from other foundations.

## Prefer Deterministic Metadata

Use `ActionMetadata`, `ActionStrategyMetadata`, and `ActionChainMetadata` for small, serializable
metadata maps. These value models sort dictionary inputs for stable `to_dict()` payloads.

## Validate Before Sharing

Call `validate()` on `UniversalAction` and use local validation helpers for value models before
passing payloads across package boundaries.

```python
from packages.action import ActionType, UniversalAction

action = UniversalAction(action_type=ActionType.TASK)

assert action.validate().is_valid
```

## Use The Right Serialization Surface

Use `UniversalAction.to_dict()` for the full deterministic Action payload. Use Platform Core
`ObjectSerializer.serialize()` when only inherited object fields are needed.

## Keep Workspaces Runtime-Only

Use `ActionWorkspace` for process-local references only. Do not treat it as a database, cache,
search index, retrieval engine, scheduler, executor, orchestrator, persistence layer, or workflow
engine.

## Preserve Dependency Direction

Action Foundation may depend on Platform Core. It may coexist with Memory, Knowledge, Context,
Reasoning, and Decision foundations, but references to those foundations should remain opaque
identifiers in Action input records.

## Stay Inside Implemented Boundaries

The implemented SDK does not include action execution, strategy execution, chain execution, outcome
computation, reference resolution, provenance evaluation, scheduling, orchestration, optimization,
persistence, search, AI integration, REST APIs, frontend behavior, autonomous behavior, or workflow
behavior.
