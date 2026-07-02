# Platform Core SDK API Reference

## Import Path

All public Platform Core SDK interfaces are exported from `packages.objects`.

```python
from packages.objects import GarudaObject, ObjectRegistry, ObjectSerializer
```

## Object Framework

### `GarudaObject`

Base platform object.

Constructor fields:

- `object_id`
- `metadata`
- `tags`
- `lifecycle_state`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`

Public properties:

- `object_id`
- `metadata`
- `tags`
- `lifecycle_state`
- `created_at`
- `updated_at`
- `created_by`
- `updated_by`
- `behaviors`
- `relationships`

Public methods:

- `register_validation_hook(hook)`
- `register_behavior(name, value)`
- `validate()`
- `transition_to(new_state)`

Class attributes:

- `object_type`
- `schema_version`
- `object_version`

### `CanonicalObject`

Base class for canonical object types. Use this when a class should be accepted by
`ObjectRegistry`.

### `Metadata`

Dataclass containing:

- `values`

### `LifecycleState`

Enum values:

- `draft`
- `active`
- `archived`

## Registry

### `ObjectRegistry`

Registry for canonical object classes.

Public methods:

- `register(object_type)`
- `lookup(object_name)`
- `lookup_by_class(object_type)`
- `enumerate()`
- `validate()`

Behavior:

- accepts `CanonicalObject` subclasses
- rejects non-canonical types
- rejects duplicate registrations

### `ObjectFactory`

Inert placeholder interface. Calling `create()` raises `NotImplementedError`.

## Serialization

### `ObjectSerializer`

Serializer for `GarudaObject` state.

Class attributes:

- `serialization_version`

Public methods:

- `serialize(obj)`
- `serialize_json(obj)`
- `deserialize(payload)`
- `deserialize_json(text)`

Serialized payload fields include:

- `serialization_version`
- `schema_version`
- `object_version`
- `object_type`
- `object_id`
- `metadata`
- `tags`
- `lifecycle_state`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`
- `behaviors`

## Relationships

### `Relationship`

Dataclass for relationship payloads between object IDs.

Fields:

- `source_object_id`
- `target_object_id`
- `relationship_type`
- `relationship_direction`
- `relationship_status`
- `metadata`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`
- `relationship_id`

Public methods:

- `to_dict()`

Limitations:

- There is no dedicated relationship deserializer API.
- Relationships refer to UUIDs and do not embed object instances.

### `RelationshipType`

Enum values:

- `owns`
- `contains`
- `references`
- `depends_on`
- `parent_of`
- `child_of`
- `related_to`

### `RelationshipDirection`

Enum values:

- `directed`
- `undirected`

### `RelationshipStatus`

Enum values:

- `active`
- `inactive`
- `deleted`

## Lifecycle Events

### `LifecycleEvent`

Dataclass for lifecycle event payloads.

Fields:

- `related_object_id`
- `event_type`
- `event_timestamp`
- `event_actor`
- `event_metadata`
- `event_version`
- `event_id`

Public methods:

- `to_dict()`

Limitations:

- There is no dedicated lifecycle event deserializer API.
- Lifecycle events do not publish to an event bus.

### `LifecycleEventType`

Enum values:

- `object_created`
- `object_updated`
- `object_activated`
- `object_suspended`
- `object_archived`
- `object_deleted`
- `validation_failed`
- `relationship_added`
- `relationship_removed`
- `behavior_changed`
- `version_changed`

## Validation

### `ValidationResult`

Dataclass containing:

- `errors`

Public properties:

- `is_valid`

Public methods:

- `add_error(...)`
- `add_warning(...)`
- `merge(other)`

### `ValidationError`

Dataclass containing:

- `message`
- `category`
- `severity`
- `field`
- `code`
- `context`

### `ValidationSeverity`

Enum values:

- `info`
- `warning`
- `error`
- `critical`

### `ValidationCategory`

Enum values:

- `identity`
- `metadata`
- `lifecycle`
- `behavior`
- `relationships`
- `schema`
- `version`

### Validation Helpers

Public helper functions:

- `validate_object(obj)`
- `validate_object_identity(obj)`
- `validate_object_metadata(obj)`
- `validate_object_lifecycle(obj)`
- `validate_object_behavior(obj)`
- `validate_object_relationships(obj)`
- `validate_object_schema(obj)`
- `validate_object_version(obj)`
