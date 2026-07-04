# Knowledge Foundation SDK API Reference

## Import Path

All public Knowledge Foundation SDK interfaces are exported from `packages.knowledge`.

```python
from packages.knowledge import UniversalKnowledge, KnowledgeReferenceStore
```

## Universal Knowledge

### `UniversalKnowledge`

Platform-level Knowledge object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `knowledge_type`
- `knowledge_state`
- `confidence`
- `knowledge_metadata`
- `evidence`
- `provenance`
- inherited Platform Core object fields

Public properties:

- `knowledge_type`
- `knowledge_state`
- `confidence`
- `knowledge_metadata`
- `evidence`
- `provenance`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `KnowledgeType`

Enum values:

- `fact`
- `concept`
- `principle`
- `rule`
- `observation`

### `KnowledgeState`

Enum values:

- `draft`
- `supported`
- `validated`
- `established`
- `superseded`
- `archived`

### `KnowledgeConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `KnowledgeMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Evidence And Provenance

### `EvidenceType`

Enum values:

- `memory_reference`
- `document_reference`
- `external_reference`
- `observation_reference`
- `certified_evidence`

### `EvidenceReference`

Frozen dataclass fields:

- `reference_type`
- `reference_identifier`
- `reference_label`
- `reference_metadata`

Public methods:

- `to_dict()`

### `KnowledgeEvidence`

Frozen dataclass fields:

- `references`
- `evidence_metadata`

Public methods:

- `to_dict()`

### `KnowledgeOrigin`

Enum values:

- `validated_memory`
- `verified_observation`
- `external_reference`
- `human_curation`
- `system_fact`

### `KnowledgeProvenance`

Frozen dataclass fields:

- `origin`
- `creator`
- `created_at`
- `evidence_references`
- `provenance_metadata`

Public methods:

- `to_dict()`

## Classification Contract

### `KnowledgeCategory`

Enum values:

- `factual`
- `conceptual`
- `procedural`
- `structural`
- `observational`

### `ClassificationDimension`

Frozen dataclass fields:

- `dimension_name`
- `dimension_value`
- `dimension_metadata`

Public methods:

- `to_dict()`

### `ClassificationMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ClassificationDescriptor`

Frozen dataclass fields:

- `category`
- `dimensions`
- `classification_metadata`

Public methods:

- `to_dict()`

### `KnowledgeClassificationContract`

Frozen dataclass fields:

- `supported_categories`
- `supported_dimensions`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Query Contract

### `QueryType`

Enum values:

- `exact_identifier`
- `category`
- `classification`
- `provenance`
- `evidence`
- `metadata`

### `QueryConstraint`

Frozen dataclass fields:

- `constraint_type`
- `operator`
- `value`
- `constraint_metadata`

Public methods:

- `to_dict()`

### `QueryMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `KnowledgeQuery`

Frozen dataclass fields:

- `query_type`
- `constraints`
- `metadata`

Public methods:

- `to_dict()`

### `KnowledgeQueryContract`

Frozen dataclass fields:

- `supported_query_types`
- `supported_constraint_types`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Reference Store

### `KnowledgeReferenceStore`

Process-local reference container for `UniversalKnowledge`.

Public methods:

- `add(knowledge)`
- `get(knowledge_id)`
- `remove(knowledge_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

### `StoreStatistics`

Frozen dataclass fields:

- `total_knowledge_objects`
- `created_at`
- `last_modified_at`

Public methods:

- `to_dict()`

## Validation Helpers

The Knowledge package exports validation helpers for implemented Knowledge value objects,
contracts, and the runtime reference store. These helpers return Platform Core `ValidationResult`
instances and do not introduce a separate validation engine.
