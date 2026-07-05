# Decision Foundation SDK Best Practices

## Use Decision Objects As Records

Use `UniversalDecision` to record decision state, outcome, confidence, metadata, inputs, and
provenance. Do not use it as an executor or workflow engine.

## Keep References Opaque

Use `DecisionInputReference.identifier` and `DecisionStepReference.decision_identifier` as opaque
strings. Store identifiers, not live objects from other foundations.

## Prefer Deterministic Metadata

Use `DecisionMetadata`, `DecisionStrategyMetadata`, and `DecisionChainMetadata` for small,
serializable metadata maps. These value models sort dictionary inputs for stable `to_dict()`
payloads.

## Validate Before Sharing

Call `validate()` on `UniversalDecision` and use local validation helpers for value models before
passing payloads across package boundaries.

```python
from packages.decision import DecisionType, UniversalDecision

decision = UniversalDecision(decision_type=DecisionType.RECOMMENDATION)

assert decision.validate().is_valid
```

## Use The Right Serialization Surface

Use `UniversalDecision.to_dict()` for the full deterministic Decision payload. Use Platform Core
`ObjectSerializer.serialize()` when only inherited object fields are needed.

## Keep Workspaces Runtime-Only

Use `DecisionWorkspace` for process-local references only. Do not treat it as a database, cache,
search index, retrieval engine, or persistence layer.

## Preserve Dependency Direction

Decision Foundation may depend on Platform Core. It may coexist with Memory, Knowledge, Context, and
Reasoning, but references to those foundations should remain opaque identifiers in Decision input
records.

## Stay Inside Implemented Boundaries

The implemented SDK does not include decision execution, strategy execution, chain execution,
outcome computation, reference resolution, provenance evaluation, orchestration, planning,
optimization, persistence, search, AI integration, REST APIs, frontend behavior, autonomous
behavior, or workflow behavior.
