# Reasoning Foundation SDK Best Practices

## Prefer UniversalReasoning For Reasoning Records

Use `UniversalReasoning` for platform-level Reasoning objects. It carries Platform Core identity,
metadata, tags, lifecycle state, validation hooks, audit fields, behaviors, and relationship
storage.

## Keep Identifiers Opaque

Use strings for reasoning input identifiers and reasoning step identifiers. Do not assume the SDK
resolves those identifiers into Memory, Knowledge, Context, or Reasoning objects.

## Use to_dict For Reasoning Payloads

Use `UniversalReasoning.to_dict()` when a deterministic Reasoning payload is required.

Use Platform Core `ObjectSerializer.serialize()` when inherited Platform Core fields are enough.

## Keep Contracts Descriptive

Use `ReasoningStrategy`, `ReasoningStrategyContract`, `ReasoningChain`, and
`ReasoningChainContract` to record intent and structure. Do not treat them as engines. They do not
execute, infer, generate conclusions, plan, decide, orchestrate, search, retrieve, rank, or persist.

## Use ReasoningWorkspace For Runtime References Only

Use `ReasoningWorkspace` to keep `UniversalReasoning` references in memory for the current process.
Store only `UniversalReasoning` instances and use exact identifiers for lookup and removal.

Do not treat `ReasoningWorkspace` as a database, cache, retrieval engine, search engine,
or durable store.

## Validate Before Sharing Payloads

Call `validate()` on `UniversalReasoning` and `ReasoningWorkspace` before using their payloads in a
certified flow. Use exported validation helpers for inputs, provenance, strategies, chains, and
statistics models.

## Preserve Dependency Direction

Reasoning may coexist with Platform Core, Memory Foundation, Knowledge Foundation, and Context
Foundation. Do not make those foundations depend on Reasoning through SDK usage.

## Avoid Future-Feature Language In Implemented Code Paths

Do not describe reasoning engines, strategy execution, chain execution, inference, conclusion
generation, planning, decision making, orchestration, AI, persistence, search, REST, frontend, or
workflow systems as available SDK capabilities.
