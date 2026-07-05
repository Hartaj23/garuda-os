# Universal Decision Framework

## Implementation Summary

GAR-SPRINT-0007 Mission Alpha adds the service-independent Universal Decision Framework under
`packages/decision`.

The implementation is intentionally narrow:

- no existing foundation package is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no execution behavior is introduced

## Public Interface

Import Decision Foundation interfaces from `packages.decision`.

```python
from packages.decision import DecisionType, UniversalDecision

decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
)
```

## Value Models

`DecisionConfidence` and `DecisionMetadata` are frozen dataclasses.

`DecisionConfidence` accepts these levels:

- `unknown`
- `low`
- `medium`
- `high`

`DecisionMetadata` stores dictionary or tuple input in deterministic sorted order and returns a
plain dictionary through `to_dict()`.

## Validation

`UniversalDecision` registers the local `validate_decision` hook. Validation returns Platform Core
`ValidationResult` values and checks Decision-specific field types.

Do not add a Decision validation engine. Future validation additions require architecture approval
and must preserve Platform Core compatibility.

## Serialization

Use `UniversalDecision.to_dict()` for deterministic Decision payloads.

Use Platform Core `ObjectSerializer.serialize()` when inherited Platform Core fields are sufficient.
`ObjectSerializer` is unchanged by this mission.

## Platform Compatibility

`UniversalDecision` inherits `CanonicalObject`, so it preserves:

- object identity
- metadata
- tags
- lifecycle state
- created and updated audit fields
- validation hooks
- relationship storage
- behavior registry

## Engineering Boundaries

Do not add decision engine behavior, autonomous decision making, planning, workflow behavior,
orchestration, optimization, persistence, search, AI behavior, REST APIs, frontend behavior or
execution behavior to this framework.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
Reasoning Foundation for Mission Alpha.

## Verification

Mission Alpha is verified by `tests/test_universal_decision_framework.py`, which covers
construction, immutability, deterministic payloads, validation, Platform Core compatibility,
foundation coexistence and explicit absence of future behavior.
