# Runtime Foundation SDK Practical Examples

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Example 1 — Runtime Foundation Construction

**Referenced symbols:** `RuntimeFoundation`, `RuntimeFoundationCategory`

**Related mission(s):** Alpha

**Related certification scenario(s):** 1, 4, 5

```python
from packages.runtime import RuntimeFoundation, RuntimeFoundationCategory

foundation = RuntimeFoundation(foundation_category=RuntimeFoundationCategory.CORE)
assert foundation.validate().is_valid
```

## Example 2 — Dual Subordination Contract

**Referenced symbols:** `CanonicalRuntimeContract`, `build_integration_subordination`, `build_interface_subordination`

**Related mission(s):** Bravo

**Related certification scenario(s):** 7, 11

```python
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    build_interface_subordination as build_integration_interface_subordination,
)
from packages.interface import CanonicalInterfaceRequest, InterfaceContractMetadata
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeContextReference,
    RuntimeContextReferenceCollection,
    RuntimeContractMetadata,
    build_integration_subordination,
    build_interface_subordination,
)

interface_request = CanonicalInterfaceRequest(
    contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
    # ... remaining required Interface fields
)
integration_contract = CanonicalIntegrationContract(
    contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
    interface_subordination=build_integration_interface_subordination(interface_request),
    # ... remaining required Integration fields
)
contract = CanonicalRuntimeContract(
    contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
    integration_subordination=build_integration_subordination(integration_contract),
    interface_subordination=build_interface_subordination(interface_request),
    context_references=RuntimeContextReferenceCollection(
        references=(RuntimeContextReference(context_identifier="context:example"),),
    ),
    # ... remaining required CanonicalObject fields
)
assert contract.integration_subordination.is_subordinate_to(integration_contract)
assert contract.interface_subordination.is_subordinate_to(interface_request)
```

## Example 3 — Boundary And Lifecycle Metadata

**Referenced symbols:** `RuntimeBoundaryModel`, `RuntimeArtifactLifecycle`

**Related mission(s):** Charlie

**Related certification scenario(s):** 6, 11

```python
from packages.runtime import (
    RuntimeArtifactLifecycle,
    RuntimeBoundaryExclusivity,
    RuntimeBoundaryModel,
    RuntimeBoundarySide,
    RuntimeLifecycleState,
)

boundary = RuntimeBoundaryModel(
    boundary_identifier="runtime-stack-traversal",
    boundary_side=RuntimeBoundarySide.STACK_TRAVERSAL,
    exclusivity=RuntimeBoundaryExclusivity(
        traverses_integration_foundation=True,
        traverses_interface_foundation=True,
    ),
)
lifecycle = RuntimeArtifactLifecycle(
    runtime_lifecycle_state=RuntimeLifecycleState.ACTIVE,
    boundary_descriptor=boundary.to_descriptor(),
    artifact_reference="artifact:example",
)
assert lifecycle.validate().is_valid
```

## Example 4 — Context Classification Evaluation

**Referenced symbols:** `evaluate_runtime_context_classification`, `RuntimeContextClassificationHook`

**Related mission(s):** Delta

**Related certification scenario(s):** 8, 9

```python
from packages.runtime import (
    RuntimeContextClassificationHook,
    RuntimeContextClassificationHookCollection,
    RuntimeContextReference,
    evaluate_runtime_context_classification,
)

primary_reference = RuntimeContextReference(context_identifier="context:primary")
evaluation = evaluate_runtime_context_classification(
    RuntimeContextClassificationHookCollection(
        hooks=(RuntimeContextClassificationHook(context_reference=primary_reference),),
    )
)
assert evaluation.is_deterministic
```

## Example 5 — Runtime Artifact Validation

**Referenced symbols:** `evaluate_runtime_artifact`, `RuntimeValidationPolicy`

**Related mission(s):** Echo

**Related certification scenario(s):** 3, 10, 13

```python
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeValidationPolicy,
    evaluate_runtime_artifact,
)

policy = RuntimeValidationPolicy()
result = evaluate_runtime_artifact(contract, policy)
assert result.is_valid
```

## Example 6 — Registry Registration And Lookup

**Referenced symbols:** `RuntimeRegistry`, `compose_runtime_registry_entry`

**Related mission(s):** Foxtrot

**Related certification scenario(s):** 8, 14

```python
from packages.runtime import (
    RuntimeContextDescriptor,
    RuntimeRegistrationContract,
    RuntimeRegistry,
    compose_runtime_registry_entry,
)

registry = RuntimeRegistry()
entry = compose_runtime_registry_entry(
    registration_contract=RuntimeRegistrationContract(
        registration_identifier="registration:example",
        # ... remaining required fields
    ),
    context_descriptor=RuntimeContextDescriptor(
        context_identifier="context:example",
        # ... remaining required fields
    ),
)
registry.register(entry)
lookup = registry.lookup_by_registration_identifier("registration:example")
assert lookup.found
```

## Example 7 — End-To-End Descriptive Pipeline

**Referenced symbols:** `RuntimeFoundation`, `CanonicalRuntimeContract`, `evaluate_runtime_artifact`, `RuntimeRegistry`

**Related mission(s):** Alpha, Bravo, Charlie, Delta, Echo, Foxtrot

**Related certification scenario(s):** 14

```python
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeFoundation,
    RuntimeFoundationCategory,
    RuntimeRegistry,
    RuntimeValidationPolicy,
    evaluate_runtime_artifact,
)

foundation = RuntimeFoundation(foundation_category=RuntimeFoundationCategory.CORE)
assert foundation.validate().is_valid

policy = RuntimeValidationPolicy()
validation = evaluate_runtime_artifact(contract, policy)
assert validation.is_valid

registry = RuntimeRegistry()
# Register composed entries following Foxtrot catalog semantics
```

This example demonstrates the certified descriptive pipeline: foundation substrate, dual
subordination contract, lifecycle metadata, classification, validation, and registry catalog —
without operational runtime execution.
