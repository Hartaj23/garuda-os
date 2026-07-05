# Action Foundation SDK Guide

## Overview

The Universal Action Foundation SDK exposes platform-neutral models for recording action intent,
state, outcome, confidence, metadata, inputs, provenance, strategy contracts, chain contracts, and
runtime action references.

All public interfaces are exported from `packages.action`.

```python
from packages.action import ActionType, ActionWorkspace, UniversalAction
```

## What Is Implemented

The implemented SDK includes:

- `UniversalAction`
- Action type, state, outcome, confidence, and metadata models
- Opaque action input references and input collections
- Descriptive action origin and provenance records
- Descriptive action strategy contracts
- Descriptive action chain contracts
- Runtime-only `ActionWorkspace`
- Local validation helpers
- Deterministic `to_dict()` payloads where supported

## What Is Not Implemented

The Action Foundation does not execute actions, compute outcomes, resolve references, evaluate
provenance, execute strategies, execute chains, schedule work, orchestrate workflows, optimize
behavior, persist records, search, expose REST APIs, provide frontend behavior, integrate AI, or
perform autonomous behavior.

## Basic Usage

```python
from packages.action import ActionType, UniversalAction

action = UniversalAction(
    action_type=ActionType.TASK,
)

assert action.validate().is_valid
assert action.to_dict()["action_type"] == "task"
```

## Deterministic Payloads

`UniversalAction.to_dict()` provides the full deterministic Action payload. Action-specific metadata
value models sort dictionary inputs for stable output.

```python
from packages.action import ActionMetadata, ActionType, UniversalAction

action = UniversalAction(
    action_type=ActionType.REVIEW,
    action_metadata=ActionMetadata(values={"z": "last", "a": "first"}),
)

assert action.to_dict()["action_metadata"] == {"a": "first", "z": "last"}
```

## Platform Core Compatibility

`UniversalAction` inherits Platform Core `CanonicalObject` behavior, including object identity,
metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(action)

assert core_payload["object_type"] == "UniversalAction"
assert core_payload["object_id"] == str(action.object_id)
```

## Runtime Workspace

`ActionWorkspace` stores `UniversalAction` references in the current Python process. It supports
exact identifier operations only.

```python
from packages.action import ActionWorkspace

workspace = ActionWorkspace()
workspace.add(action)

assert workspace.get(action.object_id) is action
assert workspace.statistics().total_actions == 1
```

The workspace is intentionally non-serializable and is not a database, cache, search index,
retrieval engine, scheduler, executor, or workflow engine.
