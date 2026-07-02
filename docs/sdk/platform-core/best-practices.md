# Platform Core SDK Best Practices

## Keep Objects Platform-Neutral

Use Platform Core objects for universal identity and structure. Do not put business, trading,
portfolio, AI, workflow, Knowledge Graph, or Memory rules into Platform Core objects.

## Prefer Canonical Subclasses For Registry Use

Only `CanonicalObject` subclasses can be registered in `ObjectRegistry`.

```python
from packages.objects import CanonicalObject


class ExampleObject(CanonicalObject):
    pass
```

Use `GarudaObject` directly when registry participation is not required.

## Validate Before And After Serialization

Validation is cheap and platform-level.

```python
from packages.objects import ObjectSerializer

before = obj.validate()
payload = ObjectSerializer.serialize(obj)
restored = ObjectSerializer.deserialize(payload)
after = restored.validate()
```

Check `is_valid` on both results when certification-grade confidence is needed.

## Treat Serialized Payloads As Deterministic State

`ObjectSerializer` sorts metadata and behavior keys. Relationship and lifecycle event payloads sort
metadata keys. This makes payload comparison suitable for tests and certification.

## Keep Relationship Payloads ID-Based

Relationships should connect object IDs, not object instances. This keeps the relationship layer
separate from persistence and object loading concerns.

## Be Clear About Lifecycle Events

Lifecycle events are deterministic payload models. They do not imply event bus publishing,
workflow execution, or event processing.

## Keep Validation Hooks Small

Validation hooks should participate in platform validation only. They may return `None`,
`ValidationError`, or `ValidationResult`, or raise an exception when exception-style validation is
intentional.

## Do Not Rely On Unimplemented Deserializers

Current relationship and lifecycle event modules do not provide dedicated deserializer APIs. If a
test needs to reconstruct those objects, use the existing constructors explicitly and keep that
reconstruction local to the test or example.

## Avoid Future-Sprint Assumptions

Do not assume:

- persistence
- REST endpoints
- database tables
- frontend validation
- event bus processing
- workflow execution
- AI reasoning
- Knowledge Graph storage
- Memory storage
- trading or portfolio semantics
