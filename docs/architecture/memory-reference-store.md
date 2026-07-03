# In-Memory Reference Store

## Scope

This document describes GAR-SPRINT-0003 Mission Foxtrot: the In-Memory Reference Store.

Mission Foxtrot provides a process-local runtime container for `UniversalMemory` object references.
It demonstrates interoperability between the Universal Memory Framework, Memory Index Contract,
Memory Retrieval Contract, and Platform Core validation without introducing persistence or search.

## Runtime purpose

`MemoryReferenceStore` keeps references to `UniversalMemory` instances for the life of the current
process. References are discarded when the process exits.

The store supports only exact identifier operations:

- add memory
- get by exact memory identifier
- remove by exact memory identifier
- enumerate identifiers
- clear references

## Relationship to retrieval contract

The store can provide opaque memory identifiers that fit `MemoryRetrievalResponse`. It does not
interpret retrieval criteria and does not implement a retrieval engine.

## Relationship to future storage engines

Future storage engines may replace or complement this reference container after separate
architecture approval. Mission Foxtrot does not define persistence, external adapters, caching, or
database behavior.

## Lifecycle

The store exists only in process memory. Store statistics are informational and describe current
runtime reference count and timestamps.

## Explicitly out of scope

- Persistent memory store
- Database
- File storage
- Search engine
- Retrieval engine
- Query engine
- Ranking
- Vector database
- Embeddings
- Knowledge graph
- Context engine
- Reasoning
- AI behavior
- REST APIs
- Frontend features
- Workflow engine
