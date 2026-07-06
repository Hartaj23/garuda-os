# Execution Foundation SDK Guide

## Overview

The Universal Execution Foundation SDK exposes platform-neutral models for recording execution intent,
state, outcome, confidence, metadata, inputs, provenance, strategy contracts, chain contracts, and
runtime execution references.

All public interfaces are exported from `packages.execution`.

```python
from packages.execution import ExecutionType, ExecutionWorkspace, UniversalExecution
```

## What Is Implemented

The implemented SDK includes:

- `UniversalExecution`
- Execution type, state, outcome, confidence, and metadata models
- Opaque execution input references and input collections
- Descriptive execution origin and provenance records
- Descriptive execution strategy contracts
- Descriptive execution chain contracts
- Runtime-only `ExecutionWorkspace`
- Local validation helpers
- Deterministic `to_dict()` payloads where supported

## What Is Not Implemented

The Execution Foundation does not execute work, compute outcomes, resolve references, evaluate
provenance, execute strategies, execute chains, schedule work, orchestrate workflows, optimize
behavior, persist records, search, expose REST APIs, provide frontend behavior, integrate AI, or
perform autonomous behavior.

## Basic Usage

```python
from packages.execution import ExecutionType, UniversalExecution

execution = UniversalExecution(
    execution_type=ExecutionType.ACTION,
)

assert execution.validate().is_valid
assert execution.to_dict()["execution_type"] == "action"
```

## Deterministic Payloads

`UniversalExecution.to_dict()` provides the full deterministic Execution payload. Execution-specific
metadata value models sort dictionary inputs for stable output.

```python
from packages.execution import ExecutionMetadata, ExecutionType, UniversalExecution

execution = UniversalExecution(
    execution_type=ExecutionType.REVIEW,
    execution_metadata=ExecutionMetadata(values={"z": "last", "a": "first"}),
)

assert execution.to_dict()["execution_metadata"] == {"a": "first", "z": "last"}
```

## Platform Core Compatibility

`UniversalExecution` inherits Platform Core `CanonicalObject` behavior, including object identity,
metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(execution)

assert core_payload["object_type"] == "UniversalExecution"
assert core_payload["object_id"] == str(execution.object_id)
```

## Runtime Workspace

`ExecutionWorkspace` stores `UniversalExecution` references in the current Python process. It supports
exact identifier operations only.

```python
from packages.execution import ExecutionWorkspace

workspace = ExecutionWorkspace()
workspace.add(execution)

assert workspace.get(execution.object_id) is execution
assert workspace.statistics().total_executions == 1
```

The workspace is intentionally non-serializable and is not a database, cache, search index,
retrieval engine, scheduler, executor, or workflow engine.
