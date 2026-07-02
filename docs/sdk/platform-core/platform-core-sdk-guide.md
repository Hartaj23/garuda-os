# Platform Core SDK Guide

## Overview

The Platform Core SDK is the developer-facing surface for the GAR-SPRINT-0002 Universal Object
System. It provides neutral object primitives, type registration, deterministic object
serialization, immutable-ID relationships, lifecycle event payloads, and platform-level validation.

The SDK lives in `packages.objects` and is service-independent. It does not depend on backend
services, frontend code, persistence, databases, REST endpoints, workflow engines, AI systems,
Knowledge Graph, Memory, trading, or portfolio modules.

## Modules Included

### Universal Object Framework

Defines `GarudaObject`, `CanonicalObject`, `Metadata`, and `LifecycleState`.

Use it for platform-neutral object identity, metadata, tags, lifecycle state, audit fields,
behavior registration, and validation hooks.

### Universal Object Registry

Defines `ObjectRegistry`.

Use it to register canonical object classes, look them up by name or class, enumerate registered
types, and verify registry contents remain canonical.

### Serialization Framework

Defines `ObjectSerializer`.

Use it to serialize and deserialize `GarudaObject` state through deterministic dictionaries or JSON.

### Universal Relationship Framework

Defines `Relationship` and relationship enums.

Use it to describe links between existing object IDs. Relationships store immutable source and
target object IDs and emit deterministic payloads.

### Lifecycle Event Framework

Defines `LifecycleEvent` and `LifecycleEventType`.

Use it to represent lifecycle-related event payloads for Universal Objects.

### Validation Framework

Defines `ValidationResult`, `ValidationError`, validation enums, and helper functions.

Use it to collect platform-level validation findings for identity, metadata, lifecycle, behavior,
relationships, schema, and version concerns.

## Import Surface

```python
from packages.objects import (
    CanonicalObject,
    GarudaObject,
    LifecycleEvent,
    LifecycleEventType,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationCategory,
    ValidationError,
    ValidationResult,
    ValidationSeverity,
)
```

## Platform Boundaries

The Platform Core SDK intentionally does not implement:

- Domain-specific business validation
- Trading or portfolio validation
- Persistence or database storage
- REST endpoints
- Frontend behavior
- Event bus publishing
- Workflow execution
- AI reasoning
- Knowledge Graph behavior
- Memory behavior

## Future Compatibility

Future sprints may extend the platform, but Platform Core code should remain neutral. Treat object
identity, deterministic payloads, registry behavior, and validation categories as stable platform
contracts unless an approved architecture change says otherwise.
