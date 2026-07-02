# Platform Core SDK Developer Guide

## Basic Workflow

The common Platform Core workflow is:

1. Define or instantiate a platform object.
2. Validate the object.
3. Register canonical object types when type discovery is needed.
4. Serialize object state when a deterministic payload is needed.
5. Use relationships to reference other objects by immutable ID.
6. Use lifecycle events to describe object lifecycle activity.

## Creating Objects

Use `GarudaObject` directly for the base platform object, or subclass `CanonicalObject` when a
canonical object type needs registry support.

```python
from packages.objects import CanonicalObject


class ExampleObject(CanonicalObject):
    pass


obj = ExampleObject(metadata={"owner": "platform"}, tags=["example"])
```

Every object receives a UUID identity, object type, schema version, object version, metadata, tags,
lifecycle state, audit timestamps, behavior storage, relationship storage, and validation hooks.

## Validating Objects

Call `validate()` on a `GarudaObject` instance.

```python
result = obj.validate()

if result.is_valid:
    print("Object passed platform validation")
```

Validation remains platform-level. It checks object structure and core invariants. It does not
perform business, trading, portfolio, persistence, AI, workflow, Knowledge Graph, or Memory
validation.

## Registering Object Types

`ObjectRegistry` accepts `CanonicalObject` subclasses only.

```python
from packages.objects import ObjectRegistry

registry = ObjectRegistry()
registry.register(ExampleObject)

assert registry.lookup("ExampleObject") is ExampleObject
```

Duplicate registrations raise `ValueError`. Non-canonical classes raise `TypeError`.

## Serializing Object State

Use `ObjectSerializer` for deterministic object payloads.

```python
from packages.objects import ObjectSerializer

payload = ObjectSerializer.serialize(obj)
restored = ObjectSerializer.deserialize(payload)
json_text = ObjectSerializer.serialize_json(obj)
```

Deserialization returns a `GarudaObject` with restored state. Unknown payload fields are ignored by
the current serializer contract.

## Working With Relationships

Relationships connect object IDs rather than embedding objects.

```python
from packages.objects import Relationship, RelationshipType

relationship = Relationship(
    source_object_id=obj.object_id,
    target_object_id=restored.object_id,
    relationship_type=RelationshipType.RELATED_TO,
    metadata={"source": "example"},
)

payload = relationship.to_dict()
```

Current relationship support provides deterministic payload generation through `to_dict()`. It does
not provide a dedicated relationship deserializer API.

## Working With Lifecycle Events

Lifecycle events record lifecycle-related object activity as deterministic payloads.

```python
from packages.objects import LifecycleEvent, LifecycleEventType

event = LifecycleEvent(
    related_object_id=obj.object_id,
    event_type=LifecycleEventType.OBJECT_CREATED,
    event_actor="developer",
)

payload = event.to_dict()
```

Current lifecycle event support provides deterministic payload generation through `to_dict()`. It
does not provide a dedicated lifecycle event deserializer API.

## Validation Hooks

Objects may register validation hooks. Hooks may return `None`, a `ValidationError`, or a
`ValidationResult`. Exception-based hooks are still supported and exceptions propagate.

```python
from packages.objects import ValidationCategory, ValidationError


def require_owner(candidate):
    if "owner" not in candidate.metadata.values:
        return ValidationError(
            message="Owner metadata is recommended.",
            category=ValidationCategory.METADATA,
        )
    return None


obj.register_validation_hook(require_owner)
result = obj.validate()
```

Keep hooks platform-neutral. Domain validation belongs to future approved modules.
