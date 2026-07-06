# Execution Foundation SDK API Reference

## Import Path

All public Execution Foundation SDK interfaces are exported from `packages.execution`.

```python
from packages.execution import ExecutionType, ExecutionWorkspace, UniversalExecution
```

## Universal Execution

### `UniversalExecution`

Platform-level Execution object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `execution_type`
- `execution_state`
- `execution_outcome`
- `execution_confidence`
- `execution_metadata`
- `execution_inputs`
- `execution_provenance`
- inherited Platform Core object fields

Public properties:

- `execution_type`
- `execution_state`
- `execution_outcome`
- `execution_confidence`
- `execution_metadata`
- `execution_inputs`
- `execution_provenance`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `ExecutionType`

Enum values:

- `action`
- `workflow`
- `procedure`
- `command`
- `review`
- `observation`

### `ExecutionState`

Enum values:

- `draft`
- `planned`
- `ready`
- `completed`
- `archived`

### `ExecutionOutcome`

Enum values:

- `succeeded`
- `failed`
- `cancelled`
- `unknown`

### `ExecutionConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `ExecutionMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Inputs And Provenance

### `ExecutionInputType`

Enum values:

- `memory`
- `knowledge`
- `context`
- `reasoning`
- `decision`
- `action`
- `external`

### `ExecutionInputReference`

Frozen dataclass fields:

- `input_type`
- `identifier`
- `reference_metadata`

Public methods:

- `to_dict()`

### `ExecutionInputCollection`

Frozen dataclass fields:

- `references`

Public methods:

- `to_dict()`

### `ExecutionOrigin`

Enum values:

- `human`
- `system`
- `imported`
- `external`
- `action`
- `unknown`

### `ExecutionProvenance`

Frozen dataclass fields:

- `origin`
- `source_identifier`
- `created_at`
- `input_references`
- `provenance_metadata`

Public methods:

- `to_dict()`

## Strategy Contract

### `ExecutionStrategyType`

Enum values:

- `manual`
- `procedural`
- `policy_based`
- `event_driven`
- `review_based`
- `unknown`

### `ExecutionStrategyMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ExecutionStrategy`

Frozen dataclass fields:

- `strategy_type`
- `name`
- `description`
- `metadata`

Public methods:

- `to_dict()`

### `ExecutionStrategyContract`

Frozen dataclass fields:

- `strategies`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Chain Contract

### `ExecutionChainType`

Enum values:

- `sequential`
- `parallel`
- `dependency`
- `review`
- `fallback`
- `unknown`

### `ExecutionChainMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ExecutionStepReference`

Frozen dataclass fields:

- `execution_identifier`
- `metadata`

Public methods:

- `to_dict()`

`ExecutionStepReference` stores opaque identifiers only. It does not embed `UniversalExecution` objects.

### `ExecutionChain`

Frozen dataclass fields:

- `chain_type`
- `steps`
- `metadata`

Public methods:

- `to_dict()`

### `ExecutionChainContract`

Frozen dataclass fields:

- `chains`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Workspace

### `WorkspaceStatistics`

Frozen dataclass fields:

- `total_executions`
- `active_executions`
- `archived_executions`

Public methods:

- `to_dict()`

### `ExecutionWorkspace`

Runtime-only process-local reference container for `UniversalExecution` objects.

Public methods:

- `add(execution)`
- `get(execution_id)`
- `remove(execution_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

`ExecutionWorkspace` intentionally has no `to_dict()` method and is not serializable.

## Validation Helpers

Public validation helpers:

- `validate_execution`
- `validate_execution_input_reference`
- `validate_execution_input_collection`
- `validate_execution_provenance`
- `validate_execution_strategy_metadata`
- `validate_execution_strategy`
- `validate_execution_strategy_contract`
- `validate_execution_chain_metadata`
- `validate_execution_step_reference`
- `validate_execution_chain`
- `validate_execution_chain_contract`
- `validate_execution_reference`
- `validate_execution_workspace`
- `validate_workspace_statistics`

Validation helpers return Platform Core `ValidationResult` values.
