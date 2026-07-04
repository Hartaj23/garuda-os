# Context Foundation SDK Practical Examples

## Create Context

```python
from packages.context import ContextType, UniversalContext

context = UniversalContext(
    context_type=ContextType.ANALYTICAL,
)
```

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

## Validate Context

```python
result = context.validate()

assert result.is_valid
```

## Serialize Context

```python
payload = context.to_dict()

assert payload["object_type"] == "UniversalContext"
assert payload["context_type"] == "analytical"
assert payload["context_source"]["source_type"] == "knowledge"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(context)

assert core_payload["object_type"] == "UniversalContext"
assert core_payload["object_id"] == str(context.object_id)
```

## Use Composition Contracts

```python
from packages.context import CompositionType, ContextComposition

composition = ContextComposition(
    composition_type=CompositionType.GROUPED,
    context_identifiers=(str(context.object_id),),
)

composition_payload = composition.to_dict()

assert composition_payload["composition_type"] == "grouped"
assert composition_payload["context_identifiers"] == [str(context.object_id)]
```

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

selection_payload = selection.to_dict()

assert selection_payload["selection_type"] == "exact_identifier"
```

## Use The Context Workspace

```python
from packages.context import ContextWorkspace

workspace = ContextWorkspace()
workspace.add(context)

assert workspace.get(context.object_id) is context
assert workspace.identifiers() == (context.object_id,)

removed = workspace.remove(context.object_id)

assert removed is context
```

## Certified End-To-End Context Flow

```python
from packages.context import (
    CompositionType,
    ContextComposition,
    ContextScope,
    ContextScopeType,
    ContextSelectionRequest,
    ContextSource,
    ContextSourceType,
    ContextType,
    ContextWorkspace,
    SelectionCriterion,
    SelectionType,
    UniversalContext,
)
from packages.objects import ObjectSerializer

context = UniversalContext(
    context_type=ContextType.ANALYTICAL,
    context_source=ContextSource(
        source_type=ContextSourceType.KNOWLEDGE,
        source_identifier="knowledge:00000000-0000-0000-0000-000000000001",
    ),
    context_scope=ContextScope(
        scope_type=ContextScopeType.TASK,
        boundary_identifier="task:mission-hotel",
    ),
)

validation = context.validate()
context_payload = context.to_dict()
core_payload = ObjectSerializer.serialize(context)

composition = ContextComposition(
    composition_type=CompositionType.GROUPED,
    context_identifiers=(str(context.object_id),),
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

workspace = ContextWorkspace()
workspace.add(context)
stored_context = workspace.get(context.object_id)
removed_context = workspace.remove(context.object_id)

assert validation.is_valid
assert context_payload["object_type"] == "UniversalContext"
assert core_payload["object_id"] == str(context.object_id)
assert composition.to_dict()["composition_type"] == "grouped"
assert selection.to_dict()["selection_type"] == "exact_identifier"
assert stored_context is context
assert removed_context is context
assert workspace.identifiers() == ()
```

This flow mirrors the certified Context Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, retrieval engine,
composition engine, selection engine, workflow, AI, Reasoning, Decision, Agent, trading, or
portfolio functionality.
