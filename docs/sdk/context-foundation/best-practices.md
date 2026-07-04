# Context Foundation SDK Best Practices

## Prefer UniversalContext For Context Records

Use `UniversalContext` for platform-level Context objects. It carries Platform Core identity,
metadata, tags, lifecycle state, validation hooks, audit fields, behaviors, and relationship
storage.

## Keep Identifiers Opaque

Use strings for source identifiers, scope boundaries, composition identifiers, and selection
criterion values. Do not assume the SDK resolves those identifiers.

## Use to_dict For Context Payloads

Use `UniversalContext.to_dict()` when a deterministic Context payload is required.

Use Platform Core `ObjectSerializer.serialize()` when inherited Platform Core fields are enough.

## Keep Contracts Descriptive

Use `ContextComposition` and `ContextSelectionRequest` to record intent. Do not treat them as
engines. They do not compose, select, search, retrieve, filter, rank, reason, infer, or persist.

## Use ContextWorkspace For Runtime References Only

Use `ContextWorkspace` to keep `UniversalContext` references in memory for the current process.
Store only `UniversalContext` instances and use exact identifiers for lookup and removal.

Do not treat `ContextWorkspace` as a database, cache, retrieval engine, search engine, or durable
store.

## Validate Before Sharing Payloads

Call `validate()` on `UniversalContext` and `ContextWorkspace` before using their payloads in a
certified flow. Use exported validation helpers for source, scope, composition, selection, and
statistics models.

## Preserve Dependency Direction

Context may coexist with Platform Core, Memory Foundation, and Knowledge Foundation. Do not make
Memory or Knowledge depend on Context through SDK usage.

## Avoid Future-Feature Language In Implemented Code Paths

Do not describe context engines, composition engines, selection engines, reasoning, inference, AI,
persistence, REST, frontend, or workflow systems as available SDK capabilities.
