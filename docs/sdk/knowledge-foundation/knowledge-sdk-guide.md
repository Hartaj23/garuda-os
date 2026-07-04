# Knowledge Foundation SDK Guide

## Overview

The Knowledge Foundation SDK provides platform-neutral Knowledge objects and descriptive contracts
implemented in `packages.knowledge`.

The SDK is built on Platform Core. `UniversalKnowledge` inherits Platform Core identity,
metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

## Import Path

All public Knowledge Foundation SDK interfaces are exported from `packages.knowledge`.

```python
from packages.knowledge import UniversalKnowledge, KnowledgeReferenceStore
```

## Core Capabilities

- Create `UniversalKnowledge` objects.
- Record knowledge confidence and metadata.
- Record descriptive evidence and provenance.
- Produce deterministic `to_dict()` payloads.
- Validate Knowledge objects through Platform Core validation.
- Define descriptive classification contracts.
- Define descriptive query contracts.
- Keep runtime references in `KnowledgeReferenceStore` by exact identifier only.

## Descriptive Contracts

Classification and query contracts are descriptive models only. They do not classify, execute
queries, search, retrieve, filter, rank, infer, reason, or persist.

## Runtime Store

`KnowledgeReferenceStore` is process-local and in-memory only. It stores `UniversalKnowledge`
object references by exact identifier and rejects duplicate identifiers and non-Knowledge objects.

## Platform Core Compatibility

Use `ObjectSerializer` from `packages.objects` when only inherited Platform Core fields are needed.
Use `UniversalKnowledge.to_dict()` when the deterministic Knowledge payload is needed.

## Out Of Scope

The SDK does not implement Knowledge Graph behavior, inference, reasoning, search, persistence,
query execution, REST APIs, frontend features, workflow behavior, AI, Context, Decision, or Agent
systems.
