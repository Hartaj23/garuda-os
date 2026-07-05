# Action Foundation SDK API Reference

## Import Path

All public Action Foundation SDK interfaces are exported from `packages.action`.

```python
from packages.action import ActionType, ActionWorkspace, UniversalAction
```

## Universal Action

### `UniversalAction`

Platform-level Action object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `action_type`
- `action_state`
- `action_outcome`
- `action_confidence`
- `action_metadata`
- `action_inputs`
- `action_provenance`
- inherited Platform Core object fields

Public properties:

- `action_type`
- `action_state`
- `action_outcome`
- `action_confidence`
- `action_metadata`
- `action_inputs`
- `action_provenance`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `ActionType`

Enum values:

- `task`
- `review`
- `approval`
- `notification`
- `command`
- `observation`

### `ActionState`

Enum values:

- `draft`
- `proposed`
- `ready`
- `completed`
- `archived`

### `ActionOutcome`

Enum values:

- `succeeded`
- `failed`
- `deferred`
- `cancelled`
- `unknown`

### `ActionConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `ActionMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Inputs And Provenance

### `ActionInputType`

Enum values:

- `memory`
- `knowledge`
- `context`
- `reasoning`
- `decision`
- `external`

### `ActionInputReference`

Frozen dataclass fields:

- `input_type`
- `identifier`
- `reference_metadata`

Public methods:

- `to_dict()`

### `ActionInputCollection`

Frozen dataclass fields:

- `references`

Public methods:

- `to_dict()`

### `ActionOrigin`

Enum values:

- `human`
- `system`
- `imported`
- `external`
- `decision`
- `unknown`

### `ActionProvenance`

Frozen dataclass fields:

- `origin`
- `source_identifier`
- `created_at`
- `input_references`
- `provenance_metadata`

Public methods:

- `to_dict()`

## Strategy Contract

### `ActionStrategyType`

Enum values:

- `manual`
- `procedural`
- `policy_based`
- `event_driven`
- `review_based`
- `unknown`

### `ActionStrategyMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ActionStrategy`

Frozen dataclass fields:

- `strategy_type`
- `name`
- `description`
- `metadata`

Public methods:

- `to_dict()`

### `ActionStrategyContract`

Frozen dataclass fields:

- `strategies`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Chain Contract

### `ActionChainType`

Enum values:

- `sequential`
- `parallel`
- `dependency`
- `review`
- `fallback`
- `unknown`

### `ActionChainMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `ActionStepReference`

Frozen dataclass fields:

- `action_identifier`
- `metadata`

Public methods:

- `to_dict()`

`ActionStepReference` stores opaque identifiers only. It does not embed `UniversalAction` objects.

### `ActionChain`

Frozen dataclass fields:

- `chain_type`
- `steps`
- `metadata`

Public methods:

- `to_dict()`

### `ActionChainContract`

Frozen dataclass fields:

- `chains`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Workspace

### `WorkspaceStatistics`

Frozen dataclass fields:

- `total_actions`
- `active_actions`
- `archived_actions`

Public methods:

- `to_dict()`

### `ActionWorkspace`

Runtime-only process-local reference container for `UniversalAction` objects.

Public methods:

- `add(action)`
- `get(action_id)`
- `remove(action_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

`ActionWorkspace` intentionally has no `to_dict()` method and is not serializable.

## Validation Helpers

Public validation helpers:

- `validate_action`
- `validate_action_input_reference`
- `validate_action_input_collection`
- `validate_action_provenance`
- `validate_action_strategy_metadata`
- `validate_action_strategy`
- `validate_action_strategy_contract`
- `validate_action_chain_metadata`
- `validate_action_step_reference`
- `validate_action_chain`
- `validate_action_chain_contract`
- `validate_action_reference`
- `validate_action_workspace`
- `validate_workspace_statistics`

Validation helpers return Platform Core `ValidationResult` values.
