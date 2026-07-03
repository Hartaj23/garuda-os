# Memory Foundation Developer Guide

## Create A Universal Memory

```python
from packages.memory import MemorySource, MemoryType, UniversalMemory

memory = UniversalMemory(
    memory_type=MemoryType.SEMANTIC,
    content="Garuda memory objects inherit Platform Core behavior.",
    source=MemorySource(source_type="manual-entry"),
)
```

`UniversalMemory` inherits identity, metadata, tags, lifecycle state, audit fields, validation
hooks, behaviors, and relationship storage from Platform Core.

## Add Source And Provenance

```python
from datetime import datetime

from packages.memory import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryOrigin,
    MemoryProvenance,
    MemorySource,
    ProvenanceMetadata,
    ProvenanceReference,
)

source = MemorySource(
    source_type="document",
    source_identifier="GAR-SPRINT-0003",
)
provenance = MemoryProvenance(
    source=source,
    recorded_at=datetime.fromisoformat("2026-07-03T00:00:00+00:00"),
    provenance_metadata=ProvenanceMetadata(
        origin=MemoryOrigin.HUMAN,
        acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
        acquisition_channel=AcquisitionChannel.DOCUMENT,
        references=(
            ProvenanceReference(
                reference_type="document",
                reference_identifier="GAR-SPRINT-0003",
            ),
        ),
    ),
)
```

Provenance references are opaque identifiers. They do not open files, call services, or resolve
external records.

## Use Confidence And Metadata

```python
from packages.memory import MemoryConfidence, MemoryMetadata

memory = UniversalMemory(
    memory_type=MemoryType.SEMANTIC,
    content="Confidence records certainty of capture.",
    source=source,
    provenance=provenance,
    confidence=MemoryConfidence.HIGH,
    memory_metadata=MemoryMetadata(values={"domain": "platform"}),
)
```

`MemoryConfidence` records certainty of the memory recording process, not truth.

## Validate Memory

```python
result = memory.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges memory-specific validation through
the existing validation hook path.

## Serialize Memory

```python
payload = memory.to_dict()

assert payload["object_type"] == "UniversalMemory"
assert payload["memory_type"] == "semantic"
```

`UniversalMemory.to_dict()` is the deterministic memory payload. Platform Core `ObjectSerializer`
also works for inherited object fields.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(memory)

assert core_payload["object_type"] == "UniversalMemory"
```

## Use The Index Contract

```python
from packages.memory import IndexContract, IndexField, IndexFieldType, IndexMetadata

contract = IndexContract(
    metadata=IndexMetadata(),
    fields=(IndexField("memory_id", IndexFieldType.UUID),),
)
```

The index contract describes fields only. It does not index, search, or retrieve memory.

## Use The Retrieval Contract

```python
from packages.memory import (
    MemoryRetrievalCriteria,
    MemoryRetrievalRequest,
    MemoryRetrievalResponse,
    RetrievalMetadata,
    RetrievalStatus,
)

request = MemoryRetrievalRequest(
    request_id="request-001",
    criteria=MemoryRetrievalCriteria(memory_types=(MemoryType.SEMANTIC,)),
)
response = MemoryRetrievalResponse(
    request_id=request.request_id,
    metadata=RetrievalMetadata(),
    status=RetrievalStatus.COMPLETED,
    memory_ids=(str(memory.object_id),),
)
```

Retrieval responses contain opaque memory identifiers only. They do not contain memory objects.

## Use The Reference Store

```python
from packages.memory import MemoryReferenceStore

store = MemoryReferenceStore()
store.add(memory)

same_memory = store.get(memory.object_id)
identifiers = store.identifiers()
removed = store.remove(memory.object_id)
```

`MemoryReferenceStore` is process-local and in-memory only. It supports exact identifier lookup and
does not persist data.
