# Platform Core SDK Extension Guide

## Supported Extensions

The Platform Core SDK supports a small set of extension points:

- subclass `CanonicalObject`
- register canonical object classes
- register validation hooks
- register behavior values
- create relationship payloads between object IDs
- create lifecycle event payloads

These are extension points inside the completed Platform Core. They are not invitations to add
future-sprint functionality.

## Extending With Canonical Objects

Use `CanonicalObject` when a class should be discoverable through `ObjectRegistry`.

```python
from packages.objects import CanonicalObject, ObjectRegistry


class ExampleObject(CanonicalObject):
    pass


registry = ObjectRegistry()
registry.register(ExampleObject)
```

Keep subclasses light. Platform Core does not define domain object behavior.

## Extending Validation

Use validation hooks when an object needs additional platform-level checks.

```python
from packages.objects import ValidationCategory, ValidationResult


def validate_platform_metadata(obj):
    result = ValidationResult()
    if not isinstance(obj.metadata.values, dict):
        result.add_error(
            "Metadata values must remain a dictionary.",
            ValidationCategory.METADATA,
        )
    return result
```

Register the hook on an object instance:

```python
obj.register_validation_hook(validate_platform_metadata)
```

Do not use validation hooks for business, trading, portfolio, AI, workflow, Knowledge Graph, or
Memory rules.

## Registering Behaviors

`register_behavior(name, value)` stores behavior values on an object.

```python
obj.register_behavior("inspect", "enabled")
```

The current SDK stores behavior values only. It does not execute behavior, orchestrate workflows, or
load plugins.

## Relationship Extension Boundary

Create relationships by referencing object IDs.

```python
from packages.objects import Relationship

relationship = Relationship(
    source_object_id=source.object_id,
    target_object_id=target.object_id,
)
```

Relationships do not create, load, persist, or validate the target objects.

## Lifecycle Event Extension Boundary

Create lifecycle events as payloads.

```python
from packages.objects import LifecycleEvent, LifecycleEventType

event = LifecycleEvent(
    related_object_id=obj.object_id,
    event_type=LifecycleEventType.OBJECT_UPDATED,
)
```

Lifecycle events do not publish themselves and do not trigger workflows.

## Future-Sprint Boundaries

The following require future approved work before they can be implemented:

- persistence
- database repositories
- REST endpoints
- event bus publishing
- workflow execution
- AI reasoning
- Knowledge Graph
- Memory
- trading logic
- portfolio logic
