# Runtime Foundation SDK API Reference

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0019](../../../GAR-0019.md) |
| Governing ADR | [ADR-0013](../../adr/ADR-0013-runtime-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0012](../../sprints/GAR-SPRINT-0012-runtime-foundation.md) |
| Repository baseline | `c0e6433` |

## Import Path

All public Runtime Foundation SDK interfaces are exported from `packages.runtime`.

```python
from packages.runtime import CanonicalRuntimeContract, RuntimeRegistry
```

The authoritative export list is `packages.runtime.__all__` (102 symbols).

---

## Foundation Core

### `RuntimeFoundation`

Platform-level Runtime Foundation object inheriting `CanonicalObject`.

### `RuntimeFoundationCategory`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeFoundationMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeIntegrationDependency`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeInterfaceDependency`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `resolve_integration_foundation_type`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `resolve_interface_foundation_type`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_foundation`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

---

## Runtime Contracts

### `ALLOWED_INTEGRATION_CONTRACT_TYPES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `ALLOWED_INTERFACE_CONTRACT_TYPES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `CanonicalRuntimeContract`

Canonical runtime contract with dual subordination to Integration and Interface contracts.

### `RuntimeContextReference`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextReferenceCollection`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContractMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeIntegrationContractSubordination`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeInterfaceContractSubordination`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `build_integration_subordination`

Build subordination metadata linking a runtime contract to a canonical integration contract.

### `build_interface_subordination`

Build subordination metadata linking a runtime contract to a canonical interface contract.

### `validate_canonical_runtime_contract`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_context_reference`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_context_reference_collection`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_contract_metadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_integration_contract_subordination`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_interface_contract_subordination`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

---

## Lifecycle and Boundary

### `ALLOWED_RUNTIME_LIFECYCLE_TRANSITIONS`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeArtifactLifecycle`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeBoundaryDescriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeBoundaryExclusivity`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeBoundaryModel`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeBoundarySide`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeLifecycleMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeLifecycleState`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_artifact_lifecycle`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_boundary_descriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_boundary_exclusivity`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_boundary_model`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_lifecycle_metadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_lifecycle_state`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_lifecycle_transition`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

---

## Classification

### `CanonicalRuntimeContextClassification`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeClassificationMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextClassification`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextClassificationEvaluation`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextClassificationHook`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextClassificationHookCollection`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `evaluate_runtime_context_classification`

Pure deterministic evaluation of runtime context classification metadata.

### `evaluate_runtime_context_classification_validation`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_canonical_runtime_context_classification`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_classification_metadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_context_classification_hook`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_context_classification_hook_collection`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

---

## Validation

### `CANONICAL_RUNTIME_ARTIFACT_TYPES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `FORBIDDEN_OPERATIONAL_OBJECT_PREFIXES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `FORBIDDEN_VARIABILITY_OBJECT_PREFIXES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeSubordinationRule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationDescriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationIssue`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationIssueCollection`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationOutcome`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationPolicy`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationRecord`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationReport`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationRule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationRuleKind`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeValidationTarget`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeVersionCompatibilityRule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `TARGET_OBJECT_TYPES`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `build_runtime_validation_report`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `compose_cross_model_runtime_validation`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `compose_runtime_validation_results`

Compose validation results with stable issue ordering.

### `evaluate_runtime_artifact`

Deterministically evaluate a canonical runtime artifact against a validation policy.

### `serialize_runtime_validation_outcome`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_artifact_version_compatibility`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_operational_runtime_exclusion`

Verify artifact naming excludes operational runtime semantics.

### `validate_runtime_subordination_requirement`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_subordination_rule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_descriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_issue`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_metadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_policy`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_record`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_report`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_validation_rule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_variability_containment`

Verify artifact naming terminates variability at the Runtime layer.

### `validate_runtime_version_compatibility_rule`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validation_result_to_outcome`

Convert Platform Core `ValidationResult` to `RuntimeValidationOutcome`.

---

## Registry

### `RuntimeContextCatalogDeclaration`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeContextDescriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeRegistrationContract`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeRegistry`

Process-local descriptive catalog for runtime context registration and lookup.

### `RuntimeRegistryEntry`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeRegistryLookupCriteria`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeRegistryLookupResult`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `RuntimeRegistryMetadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `compose_runtime_registry_entry`

Compose a registry entry from a registration contract and context descriptor.

### `validate_runtime_context_catalog_declaration`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_context_descriptor`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_registration_contract`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_registry_artifact_composition`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_registry_entry`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.

### `validate_runtime_registry_metadata`

Public Runtime Foundation SDK symbol documented at repository baseline `c0e6433`.
