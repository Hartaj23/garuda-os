# Memory Source & Provenance Framework

## Scope

This document describes GAR-SPRINT-0003 Mission Bravo: the Memory Source & Provenance Framework.

Mission Bravo strengthens the Mission Alpha Universal Memory model with standardized source and
provenance attributes. It remains a platform-only model and does not introduce storage, indexing,
retrieval, search, persistence, database integration, external service integration, embeddings,
AI behavior, reasoning, REST endpoints, frontend behavior, or workflow behavior.

## Included capabilities

- `MemoryOrigin`
- `AcquisitionMethod`
- `AcquisitionChannel`
- `ProvenanceReference`
- `ProvenanceMetadata`
- Strengthened `MemorySource`
- Strengthened `MemoryProvenance`
- Universal Memory validation integration
- Deterministic provenance payload support

## Provenance model

`MemorySource` continues to describe the immediate source descriptor for a memory. Mission Bravo
keeps this model compatible with Mission Alpha.

`MemoryProvenance` continues to attach source, recording timestamp, recording actor, and trace
metadata to `UniversalMemory`. Mission Bravo extends it with `ProvenanceMetadata`, which captures
the acquisition timestamp, origin, acquisition method, acquisition channel, and optional opaque
references.

## Trust model

Provenance records how a memory entered the platform. It does not prove that the memory is true,
complete, relevant, or useful. `MemoryConfidence` remains the certainty of the recording process,
not a truth score.

## Traceability and auditability

`ProvenanceReference` stores opaque identifiers such as document IDs, conversation IDs, or external
system IDs. These identifiers are data only. The platform model does not perform lookups, open
handles, retrieve records, or depend on external systems.

`ProvenanceMetadata` is immutable after construction so acquisition facts are not casually changed
after recording.

## Platform boundaries

Mission Bravo does not modify Platform Core object behavior. `UniversalMemory` continues to inherit
from `CanonicalObject` and reuse the existing validation hook pathway.

## Explicitly out of scope

- Memory store
- Memory index
- Retrieval engine
- Search
- Persistence
- Database integration
- Vector database integration
- External service calls
- AI inference
- Knowledge extraction
- Context generation
- Reasoning
- REST endpoints
- Frontend features
- Workflow behavior
