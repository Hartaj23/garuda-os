# Memory Foundation SDK Best Practices

## Keep Memory Platform-Neutral

Use `UniversalMemory` for platform memory records. Do not add service-specific, product-specific,
or infrastructure-specific behavior to memory objects.

## Preserve Deterministic Payloads

Use `to_dict()` when you need the memory-specific payload. Preserve explicit field ordering and
sorted nested metadata dictionaries when extending patterns in future approved work.

## Separate Contracts From Implementations

`IndexContract` and retrieval contract models are descriptive. Do not treat them as engines.

- Index contracts do not index.
- Retrieval contracts do not retrieve.
- Retrieval responses contain opaque memory identifiers only.

## Keep Provenance Explicit

Use `MemorySource`, `MemoryProvenance`, `ProvenanceMetadata`, and `ProvenanceReference` to preserve
traceability. Keep provenance references opaque and avoid coupling them to external systems.

## Use Confidence Carefully

`MemoryConfidence` records certainty of capture. It is not a truth score, relevance score, ranking
signal, or AI judgment.

## Avoid Persistence Assumptions

`MemoryReferenceStore` is process-local and in-memory only. Do not use it as a database, cache,
file store, distributed memory system, or persistent memory store.

## Respect Platform Core Boundaries

Platform Core owns object identity, lifecycle state, validation contracts, and inherited object
serialization. Memory Foundation builds on those contracts without replacing them.

## Keep Future Layers Separate

Knowledge, Context, Reasoning, Decision, and Agent layers are future architectural layers. Do not
document or use them as implemented Memory Foundation capabilities.
