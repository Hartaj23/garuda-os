# Interface Foundation SDK API Reference

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0017](../../../GAR-0017.md) |
| Governing ADR | [ADR-0011](../../adr/ADR-0011-interface-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0010](../../sprints/GAR-SPRINT-0010-interface-foundation.md) |
| Repository baseline | `d542f51` |

## Import Path

All public Interface Foundation SDK interfaces are exported from `packages.interface`.

```python
from packages.interface import CanonicalInterfaceRequest, InterfaceRegistry
```

The authoritative export list is `packages.interface.__all__` (80 symbols).

---

## Foundation Core

### `InterfaceFoundation`

Platform-level Interface Foundation object. Inherits `CanonicalObject`. Does not perform routing,
execution, or provider integration.

### `InterfaceFoundationCategory`

Enum. Values: `core`.

### `InterfaceFoundationMetadata`

Frozen dataclass metadata container with deterministic `to_dict()`.

### `validate_interface_foundation`

Validation helper for `InterfaceFoundation`. Returns Platform Core `ValidationResult`.

---

## Canonical Contracts

### `CanonicalInterfaceRequest`

Canonical request contract inheriting `CanonicalObject`. Required fields: `contract_metadata`,
`correlation`, `origin`, `context_references`, `canonical_payload`.

### `CanonicalInterfaceResponse`

Canonical response contract inheriting `CanonicalObject`. Required fields: `status`, `result`.

### `CanonicalInterfacePayload`

Frozen dataclass canonical payload values map.

### `InterfaceContractMetadata`

Frozen dataclass contract metadata container.

### `InterfaceCorrelation`

Frozen dataclass correlation identifier and optional trace metadata.

### `InterfaceOrigin`

Frozen dataclass origin identifier and optional origin metadata.

### `InterfaceContextReference`

Frozen dataclass opaque context reference.

### `InterfaceContextReferenceCollection`

Immutable tuple collection of context references.

### `InterfaceResponseStatus`

Enum. Values: `success`, `failure`, `partial`.

### `InterfaceResponseResult`

Frozen dataclass response result values map.

### `InterfaceResponseWarning`

Frozen dataclass structured warning (descriptive only).

### `InterfaceResponseError`

Frozen dataclass structured error (descriptive only).

### `InterfaceResponseErrorCollection`

Immutable tuple collection of response errors.

### `validate_canonical_interface_request`

Validation helper for `CanonicalInterfaceRequest`.

### `validate_canonical_interface_response`

Validation helper for `CanonicalInterfaceResponse`.

### `validate_canonical_interface_payload`

Validation helper for `CanonicalInterfacePayload`.

### `validate_interface_contract_metadata`

Validation helper for `InterfaceContractMetadata`.

### `validate_interface_correlation`

Validation helper for `InterfaceCorrelation`.

### `validate_interface_origin`

Validation helper for `InterfaceOrigin`.

### `validate_interface_context_reference`

Validation helper for `InterfaceContextReference`.

### `validate_interface_context_reference_collection`

Validation helper for `InterfaceContextReferenceCollection`.

### `validate_interface_response_result`

Validation helper for `InterfaceResponseResult`.

### `validate_interface_response_warning`

Validation helper for `InterfaceResponseWarning`.

### `validate_interface_response_error`

Validation helper for `InterfaceResponseError`.

### `validate_interface_response_error_collection`

Validation helper for `InterfaceResponseErrorCollection`.

---

## Lifecycle

### `InterfaceBoundaryModel`

Constitutional boundary model inheriting `CanonicalObject`. Declarative only — no routing or dispatch.

### `InterfaceBoundarySide`

Enum. Values: `external`, `membrane`.

### `InterfaceBoundaryExclusivity`

Frozen dataclass declaring single-membrane exclusivity (`single_membrane: bool`).

### `InterfaceBoundaryDescriptor`

Frozen dataclass boundary descriptor snapshot.

### `InterfaceArtifactLifecycle`

Descriptive artifact lifecycle record inheriting `CanonicalObject`. Uses opaque `artifact_reference`.

### `InterfaceLifecycleState`

Enum. Values: `draft`, `active`, `suspended`, `archived`.

### `InterfaceLifecycleMetadata`

Frozen dataclass lifecycle metadata container.

### `validate_interface_boundary_model`

Validation helper for `InterfaceBoundaryModel`.

### `validate_interface_boundary_exclusivity`

Validation helper for `InterfaceBoundaryExclusivity`.

### `validate_interface_boundary_descriptor`

Validation helper for `InterfaceBoundaryDescriptor`.

### `validate_interface_artifact_lifecycle`

Validation helper for `InterfaceArtifactLifecycle`.

### `validate_interface_lifecycle_state`

Validation helper for `InterfaceLifecycleState` values.

### `validate_interface_lifecycle_metadata`

Validation helper for `InterfaceLifecycleMetadata`.

---

## Translation

### `ExternalRepresentation`

Frozen dataclass external representation at the boundary. Not valid input to validation evaluator.

### `ExternalRepresentationKind`

Enum. Values: `structured`, `opaque`, `textual`.

### `TranslationDescriptor`

Frozen dataclass inbound translation descriptor with direction and reversibility metadata.

### `TranslationDirection`

Enum. Values: `inbound_to_canonical`.

### `TranslationMetadata`

Frozen dataclass translation metadata container.

### `TranslationReversibilityDescriptor`

Frozen dataclass reversibility metadata (descriptive — no reverse translation implemented).

### `CanonicalTranslationContract`

Translation contract inheriting `CanonicalObject`. Records source representation and canonical payload.

### `normalize_to_canonical_payload`

Pure function. Normalizes `ExternalRepresentation` to `CanonicalInterfacePayload`. Inbound only.

### `validate_external_representation`

Validation helper for `ExternalRepresentation`.

### `validate_translation_descriptor`

Validation helper for `TranslationDescriptor`.

### `validate_translation_metadata`

Validation helper for `TranslationMetadata`.

### `validate_translation_reversibility_descriptor`

Validation helper for `TranslationReversibilityDescriptor`.

### `validate_canonical_translation_contract`

Validation helper for `CanonicalTranslationContract`.

---

## Validation

### `InterfaceValidationPolicy`

Frozen dataclass validation policy targeting a canonical artifact type.

### `InterfaceValidationDescriptor`

Frozen dataclass validation target descriptor.

### `InterfaceValidationTarget`

Enum. Values: `request`, `response`, `translation_contract`, `boundary_model`, `artifact_lifecycle`, `registration_contract`.

### `InterfaceValidationRecord`

Validation record inheriting `CanonicalObject`.

### `InterfaceValidationOutcome`

Frozen dataclass validation outcome snapshot.

### `InterfaceValidationMetadata`

Frozen dataclass validation metadata container.

### `InterfaceVersionCompatibilityRule`

Frozen dataclass schema and object version compatibility rule.

### `evaluate_interface_artifact`

Pure deterministic evaluator. Accepts canonical Interface artifacts and policy. Rejects external
representations.

### `compose_interface_validation_results`

Merges multiple `ValidationResult` instances.

### `validation_result_to_outcome`

Converts Platform Core `ValidationResult` to `InterfaceValidationOutcome`.

### `validate_interface_validation_policy`

Validation helper for `InterfaceValidationPolicy`.

### `validate_interface_validation_record`

Validation helper for `InterfaceValidationRecord`.

---

## Registry

### `InterfaceRegistry`

Process-local deterministic catalog. Describes artifacts only — no instantiate, execute, or resolve.

Public methods: `register`, `lookup_exact`, `lookup_by_artifact_type`, `lookup`, `identifiers`, `validate`.

### `InterfaceRegistryEntry`

Frozen dataclass immutable catalog entry.

### `InterfaceRegistryLookupCriteria`

Frozen dataclass lookup criteria.

### `InterfaceRegistryLookupResult`

Frozen dataclass deterministic lookup result snapshot.

### `InterfaceRegistrationContract`

Registration contract inheriting `CanonicalObject`.

### `InterfaceAdapterDescriptor`

Frozen dataclass descriptive adapter descriptor (not a provider implementation).

### `InterfaceCapabilityDeclaration`

Frozen dataclass descriptive capability identifier (not an execution permission).

### `InterfaceRegistryMetadata`

Frozen dataclass registry metadata container.

### `validate_interface_registration_contract`

Validation helper for `InterfaceRegistrationContract`.

### `validate_interface_adapter_descriptor`

Validation helper for `InterfaceAdapterDescriptor`.

### `validate_interface_capability_declaration`

Validation helper for `InterfaceCapabilityDeclaration`.

### `validate_interface_registry_entry`

Validation helper for `InterfaceRegistryEntry`.

### `validate_interface_registry_metadata`

Validation helper for `InterfaceRegistryMetadata`.

---

## Platform Core Integration

All `CanonicalObject` subclasses inherit:

- `object_id`, `object_type`, `schema_version`, `object_version`
- `metadata`, `tags`, `lifecycle_state`, audit fields
- `validate()`, `transition_to()`, `to_dict()`

Use `packages.objects.ObjectSerializer` for inherited serialization fields.

---

## Out of Scope

This API reference documents implemented descriptive behavior only. It does not document runtime
execution, provider integration, persistence, REST APIs, MCP integration, or orchestration.
