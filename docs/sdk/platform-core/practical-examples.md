# Platform Core SDK Practical Examples

## Create And Validate An Object

```python
from packages.objects import CanonicalObject


class ExampleObject(CanonicalObject):
    pass


obj = ExampleObject(metadata={"owner": "platform"}, tags=["example"])
result = obj.validate()

assert result.is_valid
```

## Register A Canonical Object

```python
from packages.objects import ObjectRegistry

registry = ObjectRegistry()
registry.register(ExampleObject)

assert registry.lookup("ExampleObject") is ExampleObject
```

## Serialize And Deserialize Object State

```python
from packages.objects import ObjectSerializer

payload = ObjectSerializer.serialize(obj)
restored = ObjectSerializer.deserialize(payload)

assert restored.object_id == obj.object_id
assert restored.object_type == "ExampleObject"
assert restored.validate().is_valid
```

## Create A Relationship Payload

```python
from packages.objects import Relationship, RelationshipType

source = ExampleObject()
target = ExampleObject()

relationship = Relationship(
    source_object_id=source.object_id,
    target_object_id=target.object_id,
    relationship_type=RelationshipType.RELATED_TO,
    metadata={"reason": "example"},
)

payload = relationship.to_dict()

assert payload["source_object_id"] == str(source.object_id)
assert payload["target_object_id"] == str(target.object_id)
```

Relationship payloads are deterministic. The SDK does not currently include a dedicated
relationship deserializer API.

## Create A Lifecycle Event Payload

```python
from packages.objects import LifecycleEvent, LifecycleEventType

event = LifecycleEvent(
    related_object_id=obj.object_id,
    event_type=LifecycleEventType.OBJECT_CREATED,
    event_actor="example",
    event_metadata={"source": "docs"},
)

payload = event.to_dict()

assert payload["related_object_id"] == str(obj.object_id)
assert payload["event_type"] == "object_created"
```

Lifecycle event payloads are deterministic. The SDK does not currently include a dedicated
lifecycle event deserializer API.

## Aggregate Validation Results

```python
from packages.objects import (
    ValidationCategory,
    ValidationError,
    ValidationResult,
    ValidationSeverity,
)

result = ValidationResult()
result.merge(
    ValidationError(
        message="Schema version is missing.",
        category=ValidationCategory.SCHEMA,
        severity=ValidationSeverity.ERROR,
        field="schema_version",
    )
)

assert not result.is_valid
```

## Complete Platform Core Flow

```python
from packages.objects import (
    LifecycleEvent,
    LifecycleEventType,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
)

obj = ExampleObject(metadata={"scope": "platform-core"})
related = ExampleObject()

registry = ObjectRegistry()
registry.register(ExampleObject)

relationship = Relationship(
    source_object_id=obj.object_id,
    target_object_id=related.object_id,
)

event = LifecycleEvent(
    related_object_id=obj.object_id,
    event_type=LifecycleEventType.OBJECT_CREATED,
)

validation_before = obj.validate()
payload = ObjectSerializer.serialize(obj)
restored = ObjectSerializer.deserialize(payload)
validation_after = restored.validate()

assert validation_before.is_valid
assert validation_after.is_valid
assert restored.object_id == obj.object_id
assert registry.lookup("ExampleObject") is ExampleObject
assert relationship.to_dict()["source_object_id"] == str(obj.object_id)
assert event.to_dict()["related_object_id"] == str(obj.object_id)
```

This flow mirrors the certified Platform Core integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, event bus, workflow, AI, Knowledge
Graph, Memory, trading, or portfolio functionality.
