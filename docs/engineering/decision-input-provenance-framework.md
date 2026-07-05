# Decision Input and Provenance Framework

## Implementation Summary

GAR-SPRINT-0007 Mission Bravo adds descriptive input and provenance models to the Decision
Foundation.

The implementation is intentionally narrow:

- no existing non-Decision foundation package is modified
- no Platform Core behavior is changed
- no serializer is introduced
- no validation engine is introduced
- no reference resolution or execution behavior is introduced

## Public Interface

Import Decision input and provenance interfaces from `packages.decision`.

```python
from packages.decision import (
    DecisionInputCollection,
    DecisionInputReference,
    DecisionInputType,
    DecisionOrigin,
    DecisionProvenance,
)
```

## Inputs

Use `DecisionInputReference` for opaque input references.

```python
reference = DecisionInputReference(
    input_type=DecisionInputType.KNOWLEDGE,
    identifier="knowledge:00000000-0000-0000-0000-000000000001",
)
inputs = DecisionInputCollection(references=(reference,))
```

The identifier is descriptive only. The SDK does not resolve it.

## Provenance

Use `DecisionProvenance` to record how a Decision record entered Garuda.

```python
provenance = DecisionProvenance(
    origin=DecisionOrigin.HUMAN,
    input_references=inputs.references,
)
```

Provenance is descriptive only. It does not evaluate origin quality or trust.

## UniversalDecision Integration

`UniversalDecision` accepts optional `decision_inputs` and `decision_provenance` values.

```python
decision = UniversalDecision(
    decision_type=DecisionType.RECOMMENDATION,
    decision_inputs=inputs,
    decision_provenance=provenance,
)
```

Mission Alpha constructor compatibility is preserved. Optional Bravo payload fields are appended
after the original Alpha payload fields.

## Validation

The module provides local validation helpers:

- `validate_decision_input_reference`
- `validate_decision_input_collection`
- `validate_decision_provenance`

These helpers return Platform Core `ValidationResult` values. They validate shapes and metadata
only.

## Serialization

Use `to_dict()` on input and provenance models for deterministic payloads. Use
`UniversalDecision.to_dict()` for the combined Decision payload.

Platform Core `ObjectSerializer` is unchanged and serializes inherited Platform Core fields only.

## Engineering Boundaries

Do not add decision engine behavior, reference resolution, provenance evaluation, decision
execution, outcome computation, planning, workflow behavior, orchestration, optimization,
persistence, search, AI behavior, REST APIs, frontend behavior or autonomous behavior to this
framework.

Do not modify Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation or
Reasoning Foundation for Mission Bravo.

## Verification

Mission Bravo is verified by `tests/test_decision_input_provenance_framework.py`, which covers
construction, immutability, deterministic payloads, Mission Alpha compatibility, Platform Core
compatibility, foundation coexistence and explicit absence of future behavior.
