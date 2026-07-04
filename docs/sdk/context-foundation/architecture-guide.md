# Context Foundation Architecture Guide

## Overview

The Context Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0005. It builds on Platform Core and introduces Context objects, descriptive source and
scope records, deterministic payloads, descriptive composition and selection contracts, and a
runtime workspace.

## Relationship To Platform Core

`UniversalContext` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage,
and serialization compatibility for inherited fields.

The Context Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Context models may record memory-related identifiers through `ContextSource`,
`ContextComposition`, or `ContextSelectionRequest` values. These identifiers are opaque. Context
models do not hold `UniversalMemory` instances directly, and Memory Foundation packages do not
depend on Context Foundation packages.

## Relationship To Knowledge Foundation

Context models may record knowledge-related identifiers through source, scope, composition, or
selection payloads. These identifiers are opaque. Context models do not hold `UniversalKnowledge`
instances directly, and Knowledge Foundation packages do not depend on Context Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Context object, context type, state, confidence, metadata, validation
- `source.py`: context source types and deterministic source records
- `scope.py`: context scope types and deterministic scope records
- `composition.py`: descriptive composition contract models
- `selection.py`: descriptive selection contract models
- `workspace.py`: process-local exact identifier Context workspace

## Contract Separation

Composition and selection modules define contracts only.

The composition contract describes composition intent over opaque context identifiers. It does not
compose or resolve contexts.

The selection contract describes selection intent. It does not execute, search, retrieve, filter, or
rank.

## Runtime Workspace

`ContextWorkspace` is an in-memory reference container. It keeps `UniversalContext` references in
the current Python process and supports add, exact identifier get, exact identifier remove,
identifier enumeration, clear, statistics, and validation.

It is not a persistent store.

## Platform Integration Certification

The implemented Context Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
Knowledge Foundation coexistence, composition contracts, selection contracts, and the workspace.

## Relationship To Future Architecture

Future Reasoning, Decision, and Agent layers may build above the Context Foundation after separate
architecture approval. They are not implemented by this SDK.

Future persistent storage, context engines, selection engines, composition engines, search engines,
and reasoning systems are also outside the implemented Context Foundation.

## Constitutional Constraints

The Context Foundation preserves these constraints:

- Context remains platform-neutral.
- Source and scope remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Composition execution, selection execution, search, persistence, reasoning, AI, and workflow
  behavior remain out of scope.
