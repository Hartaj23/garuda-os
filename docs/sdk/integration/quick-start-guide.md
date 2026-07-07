# Integration Foundation SDK Quick Start Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Prerequisites

- Published repository baseline `121365c` or later Integration Foundation commit
- Python environment with Project Garuda dependencies installed
- Familiarity with Platform Core `CanonicalObject` and `ValidationResult`

## Step 1 — Import the public package

```python
from packages.integration import IntegrationFoundation
```

Verify exports with `packages.integration.__all__`.

## Step 2 — Build a subordinate integration contract

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
assert contract.validate().is_valid
```

## Step 3 — Validate before use

```python
from packages.integration import (
    IntegrationValidationPolicy,
    IntegrationValidationTarget,
    evaluate_integration_artifact,
)

policy = IntegrationValidationPolicy(
    policy_identifier="integration-contract:v1",
    validation_target=IntegrationValidationTarget.CONTRACT,
    target_object_type="CanonicalIntegrationContract",
)
result = evaluate_integration_artifact(contract, policy)
assert result.is_valid
```

## Step 4 — Register descriptive catalog metadata

```python
from packages.integration import (
    IntegrationParticipantDescriptor,
    IntegrationRegistrationContract,
    IntegrationRegistry,
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
```

## Next Steps

1. Read [Developer Guide](developer-guide.md) for end-to-end patterns.
2. Review [Architecture Guide](architecture-guide.md) for dependency boundaries.
3. Use [Practical Examples](practical-examples.md) for mission-aligned patterns.
4. Consult [Troubleshooting Guide](troubleshooting-guide.md) when validation or registry operations fail.
