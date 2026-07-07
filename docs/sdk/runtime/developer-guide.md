# Runtime Foundation SDK Developer Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Developer Onboarding

Welcome to the Runtime Foundation SDK. This guide orients new engineers to the certified Runtime
Foundation published through GAR-SPRINT-0012 Missions Alpha–Golf.

Recommended first steps:

1. Read [Runtime SDK Guide](runtime-sdk-guide.md) for constitutional context.
2. Read [Tripartite Distinction Guide](tripartite-distinction-guide.md) for boundary clarity.
3. Read [Architecture Guide](architecture-guide.md) for ADR-0013 principles.
4. Work through [Practical Examples](practical-examples.md) for constructible patterns.
5. Consult [API Reference](api-reference.md) for symbol details.
6. Review Golf certification evidence in GAR-CERT-S12-001 for verified behavior.

## Repository Navigation

| Path | Purpose |
| --- | --- |
| `packages/runtime/core/` | Runtime Foundation substrate |
| `packages/runtime/contracts/` | Runtime contracts with dual subordination |
| `packages/runtime/lifecycle/` | Boundary model and artifact lifecycle |
| `packages/runtime/classification/` | Context classification semantics |
| `packages/runtime/validation/` | Deterministic artifact evaluation |
| `packages/runtime/registry/` | Descriptive context catalog |
| `docs/architecture/runtime/` | Architecture documentation |
| `docs/engineering/runtime/` | Engineering documentation |
| `docs/sdk/runtime/` | This SDK documentation set |
| `docs/sprints/GAR-SPRINT-0012-runtime-certification.md` | Golf certification record |

## Public Import Path

```python
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeRegistry,
    evaluate_runtime_artifact,
    evaluate_runtime_context_classification,
)
```

The authoritative public export list is `packages.runtime.__all__` (102 symbols). See
[API Reference](api-reference.md).

## Stack Integration Walkthrough

The lawful external-capability stack traversal is Interface → Integration → Runtime. Runtime contracts
require dual subordination to both predecessor foundations.

### Step 1 — Interface Foundation

Construct a canonical interface request at the membrane boundary:

```python
from packages.interface import CanonicalInterfaceRequest, InterfaceContractMetadata

interface_request = CanonicalInterfaceRequest(
    contract_metadata=InterfaceContractMetadata(values={"channel": "membrane"}),
    # ... remaining required fields per Interface SDK
)
```

### Step 2 — Integration Foundation

Build an integration contract subordinate to the interface request:

```python
from packages.integration import (
    CanonicalIntegrationContract,
    IntegrationContractMetadata,
    build_interface_subordination as build_integration_interface_subordination,
)

integration_contract = CanonicalIntegrationContract(
    contract_metadata=IntegrationContractMetadata(values={"governance": "integration"}),
    interface_subordination=build_integration_interface_subordination(interface_request),
    # ... remaining required fields per Integration SDK
)
```

### Step 3 — Runtime Foundation

Build a runtime contract with dual subordination:

```python
from packages.runtime import (
    CanonicalRuntimeContract,
    RuntimeContractMetadata,
    RuntimeContextReferenceCollection,
    RuntimeContextReference,
    build_integration_subordination,
    build_interface_subordination,
)

runtime_contract = CanonicalRuntimeContract(
    contract_metadata=RuntimeContractMetadata(values={"governance": "runtime"}),
    integration_subordination=build_integration_subordination(integration_contract),
    interface_subordination=build_interface_subordination(interface_request),
    context_references=RuntimeContextReferenceCollection(
        references=(RuntimeContextReference(context_identifier="context:example"),),
    ),
    # ... remaining required CanonicalObject fields
)
```

This walkthrough uses import-only predecessor dependencies. Do not modify `packages/interface` or
`packages/integration` when consuming Runtime Foundation types.

## Platform Core Inheritance

Canonical Runtime Foundation artifacts inherit Platform Core `CanonicalObject`:

- `RuntimeFoundation`
- `CanonicalRuntimeContract`
- `RuntimeBoundaryModel`
- `RuntimeArtifactLifecycle`
- `CanonicalRuntimeContextClassification`
- `RuntimeValidationRecord`
- `RuntimeRegistrationContract`

Use `validate()` for Platform Core validation hooks and `ObjectSerializer.serialize()` for inherited
serialization fields.

## Dual Subordination

Runtime contracts must remain subordinate to both canonical integration contracts and canonical
interface contracts through `RuntimeIntegrationContractSubordination` and
`RuntimeInterfaceContractSubordination`. Use `build_integration_subordination()` and
`build_interface_subordination()` to construct lawful links.

## Cognitive Independence

Runtime Foundation production modules depend on Platform Core, Interface Foundation, Integration
Foundation (lawful consumption only), and other Runtime submodules. They do not import Memory,
Knowledge, Context, Reasoning, Decision, Action, or Execution packages.

## Descriptive Usage Model

Runtime Foundation types describe architectural metadata. They do not invoke providers, execute
operational runtime behavior, perform persistence, or route messages.

## Extension Principles

Approved extensions follow constitutional engineering:

1. Obtain architectural approval before implementation.
2. Extend only within the approved mission scope.
3. Preserve Platform Core inheritance and determinism.
4. Do not introduce operational runtime, provider, or persistence behavior without separate
   constitutional authority.

See [Extension Guide](extension-guide.md) for the full governance workflow.
