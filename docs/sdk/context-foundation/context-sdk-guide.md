# Context Foundation SDK Guide

## Overview

The Context Foundation SDK provides platform-level Context objects and descriptive contracts for
representing Context source, scope, composition intent, selection intent, and runtime Context
references.

The SDK is implemented in `packages.context` and builds on Platform Core object behavior. It is
service-independent and infrastructure-independent.

## Import Path

```python
from packages.context import ContextType, UniversalContext
```

All public Context Foundation interfaces are exported from `packages.context`.

## Core Flow

1. Create a `UniversalContext`.
2. Optionally attach `ContextSource` and `ContextScope`.
3. Validate through inherited Platform Core validation.
4. Serialize with `to_dict()` for the deterministic Context payload.
5. Use `ObjectSerializer.serialize()` when only inherited Platform Core fields are needed.
6. Use `ContextComposition` and `ContextSelectionRequest` to describe intent.
7. Use `ContextWorkspace` for process-local exact identifier references.

## Implemented Surface

The implemented SDK includes:

- `UniversalContext`
- `ContextType`
- `ContextState`
- `ContextConfidence`
- `ContextMetadata`
- `ContextSource`
- `ContextSourceType`
- `ContextScope`
- `ContextScopeType`
- `ContextComposition`
- `ContextCompositionContract`
- `CompositionType`
- `CompositionMetadata`
- `ContextSelectionRequest`
- `ContextSelectionContract`
- `SelectionType`
- `SelectionCriterion`
- `SelectionMetadata`
- `ContextWorkspace`
- `WorkspaceStatistics`
- validation helpers exported from `packages.context`

## Contract Boundaries

Composition and selection models describe intent only. They do not compose, select, retrieve,
filter, rank, search, reason, infer, persist, or execute.

`ContextWorkspace` is a runtime reference container. It stores `UniversalContext` references by
exact identifier in the current process only.

## Relationship To Other Foundations

Context Foundation coexists with Platform Core, Memory Foundation, and Knowledge Foundation.
Context source identifiers, scope boundaries, composition identifiers, and selection criteria are
opaque records. The SDK does not resolve them into other platform objects.
