# Memory Foundation SDK Practical Examples

## Create A Memory

```python
from packages.memory import MemorySource, MemoryType, UniversalMemory

memory = UniversalMemory(
    memory_type=MemoryType.SEMANTIC,
    content="Garuda Memory Foundation is platform-neutral.",
    source=MemorySource(source_type="manual-entry"),
)
```

## Validate A Memory

```python
result = memory.validate()

assert result.is_valid
```

## Serialize A Memory

```python
payload = memory.to_dict()

assert payload["object_type"] == "UniversalMemory"
assert payload["memory_type"] == "semantic"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(memory)

assert core_payload["object_type"] == "UniversalMemory"
assert core_payload["object_id"] == str(memory.object_id)
```

## Use Provenance

```python
from packages.memory import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryOrigin,
    MemoryProvenance,
    ProvenanceMetadata,
)

source = MemorySource(source_type="document", source_identifier="GAR-SPRINT-0003")
provenance = MemoryProvenance(
    source=source,
    provenance_metadata=ProvenanceMetadata(
        origin=MemoryOrigin.HUMAN,
        acquisition_method=AcquisitionMethod.MANUAL_ENTRY,
        acquisition_channel=AcquisitionChannel.DOCUMENT,
    ),
)

memory = UniversalMemory(
    memory_type=MemoryType.SEMANTIC,
    content="Provenance records acquisition context.",
    source=source,
    provenance=provenance,
)
```

## Use The Memory Index Contract

```python
from packages.memory import IndexContract, IndexField, IndexFieldType, IndexMetadata

contract = IndexContract(
    metadata=IndexMetadata(),
    fields=(
        IndexField("memory_id", IndexFieldType.UUID),
        IndexField("memory_type", IndexFieldType.ENUM),
    ),
)

payload = contract.to_dict()

assert payload["fields"][0]["field_name"] == "memory_id"
```

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

assert response.memory_ids == (str(memory.object_id),)
```

## Use The Memory Reference Store

```python
from packages.memory import MemoryReferenceStore

store = MemoryReferenceStore()
store.add(memory)

assert store.get(memory.object_id) is memory
assert store.identifiers() == (memory.object_id,)

removed = store.remove(memory.object_id)

assert removed is memory
```

## Complete Memory Foundation Flow

```python
store = MemoryReferenceStore()

validation = memory.validate()
memory_payload = memory.to_dict()
core_payload = ObjectSerializer.serialize(memory)

store.add(memory)
response = MemoryRetrievalResponse(
    request_id="request-002",
    metadata=RetrievalMetadata(),
    status=RetrievalStatus.COMPLETED,
    memory_ids=(str(memory.object_id),),
)
stored_memory = store.get(memory.object_id)
removed_memory = store.remove(memory.object_id)

assert validation.is_valid
assert memory_payload["object_type"] == "UniversalMemory"
assert core_payload["object_id"] == str(memory.object_id)
assert response.memory_ids == (str(memory.object_id),)
assert stored_memory is memory
assert removed_memory is memory
assert store.identifiers() == ()
```

This flow mirrors the certified Memory Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine, workflow,
AI, Knowledge Foundation, Context, Reasoning, Decision, Agent, trading, or portfolio functionality.
