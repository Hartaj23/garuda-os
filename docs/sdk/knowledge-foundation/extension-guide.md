# Knowledge Foundation SDK Extension Guide

## Extension Boundary

The implemented Knowledge Foundation may be extended only through separately approved architecture
work. This guide documents extension boundaries for current SDK users.

## Additive Contracts

New descriptive contracts should follow the current pattern:

- immutable dataclasses or enums
- deterministic `to_dict()` payloads
- local validation helpers returning Platform Core `ValidationResult`
- no dedicated serializer
- no new validation engine
- no Platform Core modification

## Object Extensions

Future Knowledge object changes should preserve `UniversalKnowledge` constructor compatibility,
payload key ordering, Platform Core identity, lifecycle behavior, validation behavior, and
relationship storage.

## Evidence And Provenance Extensions

Evidence and provenance extensions should preserve opaque identifiers. They should not resolve
references, verify provenance, compute lineage, evaluate truth, or call external systems.

## Classification Extensions

Classification extensions should remain descriptive unless a future mission explicitly approves a
classification engine. The current classification contract must not be used as an ontology engine
or taxonomy engine.

## Query Extensions

Query extensions should remain descriptive unless a future mission explicitly approves query
execution. The current query contract must not be used as a search engine, retrieval engine,
filtering engine, ranking engine, or semantic lookup engine.

## Store Extensions

The reference store is process-local and in-memory only. Persistence, caching, external storage,
database adapters, distributed storage, and retrieval engines require separate approval.

## Compatibility Requirements

Extensions should preserve compatibility with:

- Platform Core `CanonicalObject`
- Platform Core `ObjectSerializer`
- Platform Core `ValidationResult`
- Memory Foundation opaque identifier compatibility
- existing Knowledge Foundation payloads and constructor behavior

## Out Of Scope For Current SDK

The current SDK does not implement Context, Reasoning, Decision, Agent systems, AI, search,
persistence, REST APIs, frontend features, workflow behavior, trading, or portfolio functionality.
