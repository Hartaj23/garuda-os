# Integration Foundation SDK API Reference

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Import Path

All public Integration Foundation SDK interfaces are exported from `packages.integration`.

```python
from packages.integration import CanonicalIntegrationContract, IntegrationRegistry
```

The authoritative export list is `packages.integration.__all__` (94 symbols).

---

## Foundation Core

### `IntegrationFoundation`

Platform-level Integration Foundation object inheriting `CanonicalObject`.

### `IntegrationFoundationCategory`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationFoundationMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationInterfaceDependency`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `resolve_interface_foundation_type`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_foundation`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

---

## Integration Contracts

### `ALLOWED_INTERFACE_CONTRACT_TYPES`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `CanonicalIntegrationContract`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationContractMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationContractSubordination`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantReference`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantReferenceCollection`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `build_interface_subordination`

Build subordination metadata linking an integration contract to a canonical interface contract.

### `validate_canonical_integration_contract`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_contract_metadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_contract_subordination`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_reference`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_reference_collection`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

---

## Lifecycle and Boundary

### `ALLOWED_INTEGRATION_LIFECYCLE_TRANSITIONS`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationArtifactLifecycle`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationBoundaryDescriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationBoundaryExclusivity`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationBoundaryModel`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationBoundarySide`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationLifecycleMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationLifecycleState`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_artifact_lifecycle`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_boundary_descriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_boundary_exclusivity`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_boundary_model`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_lifecycle_metadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_lifecycle_state`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_lifecycle_transition`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

---

## Relationships

### `CanonicalIntegrationRelationship`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantClassification`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantClassificationHook`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantRelationshipDescriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRelationshipEvaluation`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRelationshipKind`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRelationshipMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `evaluate_integration_relationship`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `evaluate_integration_relationship_validation`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_canonical_integration_relationship`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_classification_hook`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_relationship_descriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_relationship_metadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

---

## Validation

### `CANONICAL_INTEGRATION_ARTIFACT_TYPES`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `TARGET_OBJECT_TYPES`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationSubordinationRule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationDescriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationIssue`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationIssueCollection`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationOutcome`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationPolicy`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationRecord`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationReport`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationRule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationRuleKind`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationValidationTarget`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationVersionCompatibilityRule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `build_integration_validation_report`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `compose_cross_model_integration_validation`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `compose_integration_validation_results`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `evaluate_integration_artifact`

Pure deterministic evaluator for canonical integration artifacts under a validation policy.

### `serialize_integration_validation_outcome`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_artifact_version_compatibility`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_subordination_requirement`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_subordination_rule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_descriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_issue`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_metadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_policy`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_record`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_report`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_validation_rule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_variability_containment`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_version_compatibility_rule`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validation_result_to_outcome`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

---

## Registry

### `IntegrationParticipantCatalogDeclaration`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationParticipantDescriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRegistrationContract`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRegistry`

Process-local descriptive catalog of integration registrations.

### `IntegrationRegistryEntry`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRegistryLookupCriteria`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRegistryLookupResult`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `IntegrationRegistryMetadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `compose_integration_registry_entry`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_catalog_declaration`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_participant_descriptor`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_registration_contract`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_registry_artifact_composition`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_registry_entry`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

### `validate_integration_registry_metadata`

Public Integration Foundation SDK symbol documented at repository baseline `121365c`.

