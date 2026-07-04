# Context Foundation Developer Guide

## Create Universal Context

```python
from packages.context import ContextType, UniversalContext

context = UniversalContext(
    context_type=ContextType.ANALYTICAL,
)
```

`UniversalContext` inherits Platform Core identity, metadata, tags, lifecycle state, audit fields,
validation hooks, behaviors, and relationship storage.

## Use Confidence And Metadata

```python
from packages.context import (
    ContextConfidence,
    ContextMetadata,
    ContextState,
    ContextType,
    UniversalContext,
)

context = UniversalContext(
    context_type=ContextType.OPERATIONAL,
    context_state=ContextState.VALIDATED,
    context_confidence=ContextConfidence(level="high", rationale="certified"),
    context_metadata=ContextMetadata(values={"domain": "platform"}),
)
```

`ContextConfidence` records confidence about the Context recording. It does not perform reasoning or
truth evaluation.

## Add Source And Scope

```python
from packages.context import (
    ContextScope,
    ContextScopeType,
    ContextSource,
    ContextSourceType,
    ContextType,
    UniversalContext,
)

source = ContextSource(
    source_type=ContextSourceType.KNOWLEDGE,
    source_identifier="knowledge:00000000-0000-0000-0000-000000000001",
)
scope = ContextScope(
    scope_type=ContextScopeType.TASK,
    boundary_identifier="task:mission-hotel",
)
context = UniversalContext(
    context_type=ContextType.ANALYTICAL,
    context_source=source,
    context_scope=scope,
)
```

Source and scope records are descriptive. They do not resolve sources or enforce boundaries.

## Validate Context

```python
result = context.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Context-specific checks through the
existing validation hook path.

## Serialize Context

```python
payload = context.to_dict()

assert payload["object_type"] == "UniversalContext"
assert payload["context_type"] == "analytical"
```

`UniversalContext.to_dict()` is the deterministic Context payload.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(context)

assert core_payload["object_type"] == "UniversalContext"
assert core_payload["object_id"] == str(context.object_id)
```

`ObjectSerializer` serializes inherited Platform Core fields. It does not replace
`UniversalContext.to_dict()`.

## Use Composition Contracts

```python
from packages.context import CompositionType, ContextComposition

composition = ContextComposition(
    composition_type=CompositionType.GROUPED,
    context_identifiers=(str(context.object_id),),
)
```

Composition contracts describe composition intent. They do not compose Context objects.

## Use Selection Contracts

```python
from packages.context import (
    ContextSelectionRequest,
    SelectionCriterion,
    SelectionType,
)

selection = ContextSelectionRequest(
    selection_type=SelectionType.EXACT_IDENTIFIER,
    criteria=(
        SelectionCriterion(
            criterion_name="context_identifier",
            operator="equals",
            criterion_value=str(context.object_id),
        ),
    ),
)
```

Selection contracts describe selection intent. They do not select, retrieve, filter, rank, or
search.

## Use The Context Workspace

```python
from packages.context import ContextWorkspace

workspace = ContextWorkspace()
workspace.add(context)

same_context = workspace.get(context.object_id)
identifiers = workspace.identifiers()
removed = workspace.remove(context.object_id)
```

`ContextWorkspace` is process-local and in-memory only. It stores `UniversalContext` references and
supports exact identifier operations only.
