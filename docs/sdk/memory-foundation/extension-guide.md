# Memory Foundation SDK Extension Guide

## Safe Extension Points

Current approved extension points are limited to patterns already present in the repository:

- create `UniversalMemory` instances with additional Platform Core metadata and tags
- use validation hooks inherited from Platform Core
- create descriptive index contracts with `IndexField` and `IndexContract`
- create retrieval request and response contract objects
- use `MemoryReferenceStore` for process-local exact identifier reference storage

## Approved Inheritance Model

`UniversalMemory` inherits from Platform Core `CanonicalObject`. Future canonical cognitive objects
should follow the approved Platform Core inheritance model after separate architecture approval.

## Future Memory Store

A persistent Memory Store is not implemented. Future storage work must remain separate from
`MemoryReferenceStore` unless an approved architecture change says otherwise.

## Future Retrieval Engine

A retrieval engine is not implemented. Future retrieval behavior may use the retrieval contract
models, but behavior must not be added to those contract models without approval.

## Future Knowledge Foundation

Knowledge Foundation is not implemented. It may become a future layer above Memory Foundation, but
this SDK documents only completed Memory Foundation behavior.

## Constitutional Boundaries

Extensions must not introduce unapproved:

- persistence
- databases
- file storage
- search
- ranking or scoring
- vector databases
- embeddings
- AI behavior
- reasoning
- workflow execution
- REST or frontend behavior

## Compatibility Guidance

Preserve compatibility with:

- Platform Core object identity
- deterministic `to_dict()` payloads
- `ValidationResult`
- opaque provenance references
- opaque retrieval response identifiers
- process-local behavior of `MemoryReferenceStore`
