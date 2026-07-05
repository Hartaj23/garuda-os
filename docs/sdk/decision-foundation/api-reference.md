# Decision Foundation SDK API Reference

## Import Path

All public Decision Foundation SDK interfaces are exported from `packages.decision`.

```python
from packages.decision import DecisionType, DecisionWorkspace, UniversalDecision
```

## Universal Decision

### `UniversalDecision`

Platform-level Decision object. Inherits from Platform Core `CanonicalObject`.

Constructor fields:

- `decision_type`
- `decision_state`
- `decision_outcome`
- `decision_confidence`
- `decision_metadata`
- `decision_inputs`
- `decision_provenance`
- inherited Platform Core object fields

Public properties:

- `decision_type`
- `decision_state`
- `decision_outcome`
- `decision_confidence`
- `decision_metadata`
- `decision_inputs`
- `decision_provenance`
- inherited Platform Core properties

Public methods:

- `to_dict()`
- inherited `validate()`
- inherited `transition_to(new_state)`

### `DecisionType`

Enum values:

- `recommendation`
- `selection`
- `approval`
- `rejection`
- `deferment`
- `observation`

### `DecisionState`

Enum values:

- `draft`
- `proposed`
- `confirmed`
- `archived`

### `DecisionOutcome`

Enum values:

- `accepted`
- `rejected`
- `deferred`
- `unknown`

### `DecisionConfidence`

Frozen dataclass fields:

- `level`
- `rationale`

Public methods:

- `to_dict()`

### `DecisionMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

## Inputs And Provenance

### `DecisionInputType`

Enum values:

- `knowledge`
- `context`
- `reasoning`
- `memory`
- `external`

### `DecisionInputReference`

Frozen dataclass fields:

- `input_type`
- `identifier`
- `reference_metadata`

Public methods:

- `to_dict()`

### `DecisionInputCollection`

Frozen dataclass fields:

- `references`

Public methods:

- `to_dict()`

### `DecisionOrigin`

Enum values:

- `human`
- `automated`
- `imported`
- `external`
- `unknown`

### `DecisionProvenance`

Frozen dataclass fields:

- `origin`
- `author`
- `created_at`
- `input_references`
- `provenance_metadata`

Public methods:

- `to_dict()`

## Strategy Contract

### `DecisionStrategyType`

Enum values:

- `analytical`
- `heuristic`
- `rule_based`
- `consensus`
- `expert`
- `unknown`

### `DecisionStrategyMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `DecisionStrategy`

Frozen dataclass fields:

- `strategy_type`
- `name`
- `description`
- `metadata`

Public methods:

- `to_dict()`

### `DecisionStrategyContract`

Frozen dataclass fields:

- `strategies`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Chain Contract

### `DecisionChainType`

Enum values:

- `sequential`
- `hierarchical`
- `dependency`
- `alternative`
- `review`
- `unknown`

### `DecisionChainMetadata`

Frozen dataclass fields:

- `values`

Public methods:

- `to_dict()`

### `DecisionStepReference`

Frozen dataclass fields:

- `decision_identifier`
- `metadata`

Public methods:

- `to_dict()`

### `DecisionChain`

Frozen dataclass fields:

- `chain_type`
- `steps`
- `metadata`

Public methods:

- `to_dict()`

### `DecisionChainContract`

Frozen dataclass fields:

- `chains`
- `metadata`
- `contract_version`

Public methods:

- `to_dict()`

## Workspace

### `WorkspaceStatistics`

Frozen dataclass fields:

- `total_decisions`
- `active_decisions`
- `archived_decisions`

Public methods:

- `to_dict()`

### `DecisionWorkspace`

Runtime-only workspace for `UniversalDecision` references.

Public methods:

- `add(decision)`
- `get(decision_id)`
- `remove(decision_id)`
- `identifiers()`
- `clear()`
- `statistics()`
- `validate()`

The workspace intentionally has no `to_dict()` method.

## Validation Helpers

Public validation helpers return Platform Core `ValidationResult` values:

- `validate_decision`
- `validate_decision_input_reference`
- `validate_decision_input_collection`
- `validate_decision_provenance`
- `validate_decision_strategy_metadata`
- `validate_decision_strategy`
- `validate_decision_strategy_contract`
- `validate_decision_chain_metadata`
- `validate_decision_step_reference`
- `validate_decision_chain`
- `validate_decision_chain_contract`
- `validate_decision_reference`
- `validate_decision_workspace`
- `validate_workspace_statistics`
