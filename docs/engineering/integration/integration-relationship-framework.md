# Integration Relationship Framework

## Implementation Summary

GAR-SPRINT-0011 Mission Delta adds the integration relationship framework under
`packages/integration/relationships/`.

The implementation is intentionally limited:

- relationship semantics are descriptive metadata only
- participant classification hooks are technology-neutral taxonomy structures
- relationship evaluation is deterministic and non-operational
- no routing, delivery, registry, or validation framework behavior is introduced

## Public Interface

```python
from packages.integration import (
    CanonicalIntegrationRelationship,
    IntegrationParticipantClassification,
    IntegrationParticipantClassificationHook,
    IntegrationParticipantReference,
    IntegrationParticipantRelationshipDescriptor,
    IntegrationRelationshipKind,
    evaluate_integration_relationship,
)

descriptor = IntegrationParticipantRelationshipDescriptor(
    source_participant=IntegrationParticipantReference(
        participant_identifier="participant:00000000-0000-0000-0000-000000005001",
    ),
    target_participant=IntegrationParticipantReference(
        participant_identifier="participant:00000000-0000-0000-0000-000000005002",
    ),
    relationship_kind=IntegrationRelationshipKind.ASSOCIATED,
)

evaluation = evaluate_integration_relationship(descriptor)
```

## Relationship Evaluation

Use `evaluate_integration_relationship()` for deterministic descriptive evaluation. The helper
validates relationship descriptors and returns architectural evaluation metadata only.

## Participant Classification Hooks

Attach `IntegrationParticipantClassificationHook` values to `CanonicalIntegrationRelationship`
records to express technology-neutral participant taxonomy metadata.

## Engineering Boundaries

Do not add registry behavior, validation framework rules beyond relationship scope, runtime behavior,
scheduling, recovery, providers, operational integration, or SDK examples in Mission Delta.

Do not modify Mission Alpha, Bravo, or Charlie production modules except cumulative export wiring.

## Related Documents

- [Integration Relationship Framework Architecture Guide](../../architecture/integration/integration-relationship-framework.md)
- [Integration Foundation Overview](../../architecture/integration/overview.md)
