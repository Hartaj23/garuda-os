# Memory Foundation SDK API Reference

## Import Path

All public Memory Foundation SDK interfaces are exported from `packages.memory`.

```python
from packages.memory import UniversalMemory, MemoryReferenceStore
```

## Universal Memory

### `UniversalMemory`

Platform-level memory object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `memory_type`
- `content`
- `source`
- `provenance`
- `confidence`
- `memory_metadata`
- inherited Platform Core object fields

Public properties:

- `memory_type`
- `content`
- `source`
- `provenance`
- `confidence`
- `memory_metadata`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `MemoryType`

Enum values:

- `episodic`
- `semantic`
- `procedural`
- `declarative`

### `MemoryConfidence`

Enum values:

- `unknown`
- `low`
- `medium`
- `high`

### `MemoryMetadata`

Dataclass containing:

- `values`

Public methods:

- `to_dict()`

## Source And Provenance

### `MemorySource`

Dataclass fields:

- `source_type`
- `source_identifier`
- `source_label`
- `source_metadata`

Public methods:

- `to_dict()`

### `MemoryProvenance`

Dataclass fields:

- `source`
- `recorded_at`
- `recorded_by`
- `trace_metadata`
- `provenance_metadata`

Public methods:

- `to_dict()`

### `MemoryOrigin`

Enum values:

- `human`
- `ai`
- `system`
- `imported`
- `external_service`
- `sensor`
- `unknown`

### `AcquisitionMethod`

Enum values:

- `conversation`
- `observation`
- `import`
- `api`
- `manual_entry`
- `system_event`
- `file_import`

### `AcquisitionChannel`

Enum values:

- `chat`
- `voice`
- `document`
- `api`
- `email`
- `sensor`
- `internal_platform`

### `ProvenanceReference`

Frozen dataclass fields:

- `reference_type`
- `reference_identifier`
- `reference_label`

Public methods:

- `to_dict()`

### `ProvenanceMetadata`

Frozen dataclass fields:

- `acquisition_timestamp`
- `origin`
- `acquisition_method`
- `acquisition_channel`
- `references`

Public methods:

- `to_dict()`

## Index Contract

### `IndexFieldType`

Enum values:

- `string`
- `uuid`
- `datetime`
- `enum`
- `integer`
- `boolean`

### `IndexField`

Frozen dataclass fields:

- `field_name`
- `field_type`
- `indexable`

Public methods:

- `to_dict()`

### `IndexMetadata`

Frozen dataclass fields:

- `schema_version`
- `descriptor_version`
- `platform_compatibility`

Public methods:

- `to_dict()`

### `MemoryIndexDescriptor`

Frozen dataclass fields:

- `memory_id`
- `memory_type`
- `origin`
- `acquisition_method`
- `acquisition_channel`
- `lifecycle_state`
- `confidence`
- `created_at`

Public methods:

- `to_dict()`

### `IndexContract`

Frozen dataclass fields:

- `metadata`
- `fields`

Public methods:

- `to_dict()`

## Retrieval Contract

### `MemoryRetrievalCriteria`

Frozen dataclass fields:

- `memory_types`
- `origins`
- `acquisition_methods`
- `acquisition_channels`
- `confidence`
- `lifecycle_states`

Public methods:

- `to_dict()`

### `MemoryRetrievalRequest`

Frozen dataclass fields:

- `request_id`
- `criteria`
- `metadata`
- `schema_version`

Public methods:

- `to_dict()`

### `MemoryRetrievalResponse`

Frozen dataclass fields:

- `request_id`
- `metadata`
- `status`
- `memory_ids`

Public methods:

- `to_dict()`

### `RetrievalStatus`

Enum values:

- `pending`
- `completed`
- `empty`
- `unsupported`
- `invalid`

### `RetrievalMetadata`

Frozen dataclass fields:

- `contract_version`
- `request_timestamp`
- `response_timestamp`
- `platform_compatibility`

Public methods:

- `to_dict()`

## Reference Store

### `MemoryReferenceStore`

Process-local reference container for `UniversalMemory` instances.

Public methods:

- `add(memory)`
- `get(memory_id)`
- `remove(memory_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

### `StoreStatistics`

Frozen dataclass fields:

- `total_references`
- `created_at`
- `last_modified_at`

Public methods:

- `to_dict()`

## Validation Helpers

Public helpers include:

- `validate_memory`
- `validate_provenance_metadata`
- `validate_index_field`
- `validate_index_metadata`
- `validate_index_contract`
- `validate_retrieval_metadata`
- `validate_retrieval_criteria`
- `validate_retrieval_request`
- `validate_retrieval_response`
- `validate_memory_reference`
- `validate_reference_store`
