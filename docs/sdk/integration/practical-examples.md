# Integration Foundation SDK Practical Examples

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Example 1 — Foundation Substrate

**Referenced symbols:** `IntegrationFoundation`, `IntegrationFoundationCategory`

**Related mission(s):** Alpha

**Related certification scenario(s):** 1, 4, 5

```python
from packages.integration import IntegrationFoundation, IntegrationFoundationCategory

foundation = IntegrationFoundation(foundation_category=IntegrationFoundationCategory.CORE)
assert foundation.validate().is_valid
```

## Example 2 — Subordinate Integration Contract

**Referenced symbols:** `CanonicalIntegrationContract`, `build_interface_subordination`

**Related mission(s):** Bravo

**Related certification scenario(s):** 6, 7, 11

```python
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    IntegrationParticipantReference,
    IntegrationParticipantReferenceCollection,
    build_interface_subordination,
)
from packages.interface import CanonicalInterfaceRequest

interface_request = CanonicalInterfaceRequest(...)
contract = CanonicalIntegrationContract(
    contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
    interface_subordination=build_interface_subordination(interface_request),
    participant_references=IntegrationParticipantReferenceCollection(
        references=(IntegrationParticipantReference(participant_identifier="participant:example"),),
    ),
)
assert contract.interface_subordination.is_subordinate_to(interface_request)
```

## Example 3 — Lifecycle And Boundary Metadata

**Referenced symbols:** `IntegrationBoundaryModel`, `IntegrationArtifactLifecycle`

**Related mission(s):** Charlie

**Related certification scenario(s):** 6, 10

```python
from packages.integration import (
    IntegrationArtifactLifecycle,
    IntegrationBoundaryExclusivity,
    IntegrationBoundaryModel,
    IntegrationBoundarySide,
    IntegrationLifecycleState,
)

boundary = IntegrationBoundaryModel(
    boundary_identifier="integration-membrane-traversal",
    boundary_side=IntegrationBoundarySide.MEMBRANE_TRAVERSAL,
    exclusivity=IntegrationBoundaryExclusivity(traverses_membrane=True),
)
lifecycle = IntegrationArtifactLifecycle(
    integration_lifecycle_state=IntegrationLifecycleState.ACTIVE,
    boundary_descriptor=boundary.to_descriptor(),
    artifact_reference="artifact:example",
)
assert lifecycle.validate().is_valid
```

## Example 4 — Relationship Evaluation

**Referenced symbols:** `evaluate_integration_relationship`, `IntegrationRelationshipKind`

**Related mission(s):** Delta

**Related certification scenario(s):** 8, 9

```python
from packages.integration import (
    IntegrationParticipantReference,
    IntegrationParticipantRelationshipDescriptor,
    IntegrationRelationshipKind,
    evaluate_integration_relationship,
)

descriptor = IntegrationParticipantRelationshipDescriptor(
    source_participant=IntegrationParticipantReference(participant_identifier="participant:source"),
    target_participant=IntegrationParticipantReference(participant_identifier="participant:target"),
    relationship_kind=IntegrationRelationshipKind.ASSOCIATED,
)
evaluation = evaluate_integration_relationship(descriptor)
assert evaluation.is_directional is False
```

## Example 5 — Validation And Reporting

**Referenced symbols:** `evaluate_integration_artifact`, `build_integration_validation_report`

**Related mission(s):** Echo

**Related certification scenario(s):** 3, 10

```python
from packages.integration import (
    IntegrationValidationPolicy,
    IntegrationValidationTarget,
    build_integration_validation_report,
    evaluate_integration_artifact,
)

policy = IntegrationValidationPolicy(
    policy_identifier="integration-contract:v1",
    validation_target=IntegrationValidationTarget.CONTRACT,
    target_object_type="CanonicalIntegrationContract",
)
result = evaluate_integration_artifact(contract, policy)
report = build_integration_validation_report(result)
assert report.is_valid
```

## Example 6 — Registry Catalog

**Referenced symbols:** `IntegrationRegistry`, `compose_integration_registry_entry`

**Related mission(s):** Foxtrot

**Related certification scenario(s):** 8, 9

```python
from packages.integration import (
    IntegrationParticipantDescriptor,
    IntegrationRegistrationContract,
    IntegrationRegistry,
    IntegrationRegistryLookupCriteria,
    compose_integration_registry_entry,
)

registration = IntegrationRegistrationContract(
    registration_identifier="registration:integration-contract:v1",
    participant_descriptor=IntegrationParticipantDescriptor(
        participant_identifier="participant:example",
        artifact_object_type="CanonicalIntegrationContract",
    ),
)
registry = IntegrationRegistry()
registry.register(compose_integration_registry_entry(registration))
matches = registry.lookup(
    IntegrationRegistryLookupCriteria(artifact_object_type="CanonicalIntegrationContract")
)
assert len(matches.entries) == 1
```

## Package Import Reference

All examples import from `packages.integration`. See [API Reference](api-reference.md) for the
complete public export list.
