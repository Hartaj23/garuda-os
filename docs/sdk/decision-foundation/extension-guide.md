# Decision Foundation SDK Extension Guide

## Extension Philosophy

Extend the Decision Foundation by adding small descriptive contracts after architecture approval.
Keep contracts separate from engines and runtime behavior.

## Stable Surfaces

The current implemented surfaces are:

- `UniversalDecision`
- Decision input and provenance value models
- Decision strategy contract value models
- Decision chain contract value models
- `DecisionWorkspace`
- local validation helpers
- deterministic `to_dict()` payloads

## Constructor Compatibility

Future extensions should preserve current constructors and append optional fields after existing
fields. Existing payload keys should remain stable.

## Serialization Compatibility

Future value models should expose deterministic `to_dict()` payloads. Do not introduce a custom
Decision serializer unless a future architecture mission explicitly approves it.

## Validation Compatibility

Reuse Platform Core `ValidationResult` and `ValidationCategory`. Add local validation helpers for
new descriptive models rather than introducing a validation engine.

## Dependency Boundaries

Do not make Memory, Knowledge, Context, or Reasoning packages depend on Decision Foundation. Do not
embed live objects from those foundations in Decision input references.

## Out Of Scope Until Future Approval

The following are not implemented extension points in the current SDK:

- decision execution engines
- strategy execution
- chain execution
- outcome computation
- reference resolution
- provenance evaluation
- orchestration
- planning
- optimization
- persistence
- search
- AI integration
- REST APIs
- frontend behavior
- autonomous behavior
- workflow behavior
