# Reasoning Foundation SDK API Reference

## Import Path

All public Reasoning Foundation SDK interfaces are exported from `packages.reasoning`.

```python
from packages.reasoning import ReasoningType, ReasoningWorkspace, UniversalReasoning
```

## Universal Reasoning

### `UniversalReasoning`

Platform-level Reasoning object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `reasoning_type`
- `reasoning_state`
- `reasoning_confidence`
- `reasoning_metadata`
- `reasoning_inputs`
- `reasoning_provenance`
- inherited Platform Core object fields

Public properties:

- `reasoning_type`
- `reasoning_state`
- `reasoning_confidence`
- `reasoning_metadata`
- `reasoning_inputs`
- `reasoning_provenance`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `ReasoningType`

Enum values:

- `deductive`
- `inductive`
- `abductive`
- `comparative`
- `causal`
- `temporal`
- `dependency`
- `consistency`

### `ReasoningState`

Enum values:

- `draft`
- `evaluated`
- `validated`
- `accepted`
- `superseded`
- `archived`

### `ReasoningConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `ReasoningMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Inputs And Provenance

### `ReasoningInputType`

Enum values:

- `memory`
- `knowledge`
- `context`
- `reasoning`

### `ReasoningInputReference`

Frozen dataclass fields:

- `input_type`
- `identifier`
- `reference_metadata`

Public methods:

- `to_dict()`

### `ReasoningInputCollection`

Frozen dataclass fields:

- `references`

Public methods:

- `to_dict()`

### `ReasoningOrigin`

Enum values:

- `human_defined`
- `system_generated`
- `imported`
- `validated`
- `derived`

### `ReasoningProvenance`

Frozen dataclass fields:

- `origin`
- `creator`
- `created_at`
- `input_references`
- `provenance_metadata`

Public methods:

- `to_dict()`

## Strategy Contract

### `StrategyType`

Enum values:

- `sequential`
- `parallel`
- `comparative`
- `elimination`
- `dependency`
- `validation`

### `StrategyMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ReasoningStrategy`

Frozen dataclass fields:

- `strategy_type`
- `name`
- `description`
- `metadata`

Public methods:

- `to_dict()`

### `ReasoningStrategyContract`

Frozen dataclass fields:

- `supported_strategy_types`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Chain Contract

### `ChainType`

Enum values:

- `linear`
- `branching`
- `hierarchical`
- `dependency`
- `comparative`

### `ChainMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ReasoningStepReference`

Frozen dataclass fields:

- `identifier`
- `sequence`
- `metadata`

Public methods:

- `to_dict()`

### `ReasoningChain`

Frozen dataclass fields:

- `chain_type`
- `steps`
- `metadata`

Public methods:

- `to_dict()`

### `ReasoningChainContract`

Frozen dataclass fields:

- `supported_chain_types`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Workspace

### `WorkspaceStatistics`

Frozen dataclass fields:

- `total_reasoning_objects`
- `active_reasoning_objects`
- `archived_reasoning_objects`

Public methods:

- `to_dict()`

### `ReasoningWorkspace`

Runtime-only process-local workspace for `UniversalReasoning` references.

Public methods:

- `add(reasoning)`
- `get(reasoning_id)`
- `remove(reasoning_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

The workspace itself does not provide `to_dict()`.

## Validation Helpers

The public package exports local validation helpers for implemented models, including:

- `validate_reasoning`
- `validate_reasoning_input_reference`
- `validate_reasoning_input_collection`
- `validate_reasoning_provenance`
- `validate_reasoning_strategy`
- `validate_reasoning_strategy_contract`
- `validate_reasoning_chain`
- `validate_reasoning_chain_contract`
- `validate_reasoning_step_reference`
- `validate_reasoning_reference`
- `validate_reasoning_workspace`
- `validate_workspace_statistics`
