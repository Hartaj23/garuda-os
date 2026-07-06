# Execution Foundation SDK Best Practices

## Use Execution Objects As Records

Use `UniversalExecution` to record execution state, outcome, confidence, metadata, inputs, and
provenance. Do not use it as an executor, scheduler, orchestrator, workflow engine, or autonomous
agent.

## Keep References Opaque

Use `ExecutionInputReference.identifier` and `ExecutionStepReference.execution_identifier` as opaque
strings. Store identifiers, not live objects from other foundations.

## Prefer Deterministic Metadata

Use `ExecutionMetadata`, `ExecutionStrategyMetadata`, and `ExecutionChainMetadata` for small,
serializable metadata maps. These value models sort dictionary inputs for stable `to_dict()` payloads.

## Validate Before Sharing

Call `validate()` on `UniversalExecution` and use local validation helpers for value models before
passing payloads across package boundaries.

```python
from packages.execution import ExecutionType, UniversalExecution

execution = UniversalExecution(execution_type=ExecutionType.ACTION)

assert execution.validate().is_valid
```

## Use The Right Serialization Surface

Use `UniversalExecution.to_dict()` for the full deterministic Execution payload. Use Platform Core
`ObjectSerializer.serialize()` when only inherited object fields are needed.

## Keep Workspaces Runtime-Only

Use `ExecutionWorkspace` for process-local references only. Do not treat it as a database, cache,
search index, retrieval engine, scheduler, executor, orchestrator, persistence layer, or workflow
engine.

## Preserve Dependency Direction

Execution Foundation may depend on Platform Core. It may coexist with Memory, Knowledge, Context,
Reasoning, Decision, and Action foundations, but references to those foundations should remain opaque
identifiers in Execution input records.

## Stay Inside Implemented Boundaries

The implemented SDK does not include execution behavior, strategy execution, chain execution, outcome
computation, reference resolution, provenance evaluation, scheduling, orchestration, optimization,
persistence, search, AI integration, REST APIs, frontend behavior, autonomous behavior, or workflow
behavior.
