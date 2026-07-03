# Memory Foundation SDK Guide

## Overview

The Memory Foundation SDK is the developer-facing surface for the GAR-SPRINT-0003 Memory
Foundation. It provides platform memory objects, source and provenance records, deterministic
memory payloads, index and retrieval contracts, and a process-local reference store.

The SDK lives in `packages.memory` and is service-independent. It does not depend on backend
services, frontend code, persistence, databases, REST endpoints, workflow engines, AI systems,
Knowledge Foundation implementation, trading, or portfolio modules.

## Modules Included

### Universal Memory Framework

Defines `UniversalMemory`, `MemoryType`, `MemoryConfidence`, and `MemoryMetadata`.

Use it to create platform-level memory objects that inherit from Platform Core `CanonicalObject`.

### Source And Provenance Framework

Defines `MemorySource`, `MemoryProvenance`, `MemoryOrigin`, `AcquisitionMethod`,
`AcquisitionChannel`, `ProvenanceReference`, and `ProvenanceMetadata`.

Use it to record where a memory came from and how it entered the platform.

### Serialization And Validation Integration

`UniversalMemory.to_dict()` provides the deterministic memory payload. `UniversalMemory.validate()`
uses inherited Platform Core validation plus memory-specific validation hooks.

### Memory Index Contract

Defines `IndexFieldType`, `IndexField`, `IndexMetadata`, `MemoryIndexDescriptor`, and
`IndexContract`.

Use it to describe what memory attributes may be indexed by future systems. It does not implement
an indexing engine.

### Memory Retrieval Contract

Defines `MemoryRetrievalCriteria`, `MemoryRetrievalRequest`, `MemoryRetrievalResponse`,
`RetrievalStatus`, and `RetrievalMetadata`.

Use it to describe future retrieval request and response contracts. It does not retrieve memories.

### In-Memory Reference Store

Defines `MemoryReferenceStore` and `StoreStatistics`.

Use it as a process-local runtime container for `UniversalMemory` references. It supports exact
identifier operations only and does not persist data.

## Import Surface

```python
from packages.memory import (
    MemoryReferenceStore,
    MemorySource,
    MemoryType,
    UniversalMemory,
)
```

## Platform Boundaries

The Memory Foundation SDK intentionally does not implement:

- Persistent memory storage
- Database behavior
- File storage
- Search or query language
- Retrieval engine behavior
- Ranking or scoring
- Vector databases or embeddings
- Knowledge Foundation behavior
- Context, Reasoning, Decision, or Agent layers
- REST endpoints
- Frontend behavior
- Workflow execution

## SDK Map

- Use `UniversalMemory` for memory object identity and payloads.
- Use source and provenance models for traceability.
- Use validation helpers to verify memory, provenance, index, retrieval, and store contracts.
- Use `ObjectSerializer` from `packages.objects` for inherited Platform Core fields.
- Use `MemoryReferenceStore` only for process-local references and exact identifier lookup.
