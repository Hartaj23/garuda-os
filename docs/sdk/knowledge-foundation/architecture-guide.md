# Knowledge Foundation Architecture Guide

## Overview

The Knowledge Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0004. It builds on Platform Core and introduces Knowledge objects, descriptive evidence
and provenance records, deterministic payloads, descriptive contracts, and a runtime reference
store.

## Relationship To Platform Core

`UniversalKnowledge` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage,
and serialization compatibility for inherited fields.

The Knowledge Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Knowledge models may reference memory through opaque identifiers in evidence records. Knowledge
models do not hold `UniversalMemory` instances directly, and Memory Foundation packages do not
depend on Knowledge Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Knowledge object, knowledge type, state, confidence, metadata, validation
- `evidence.py`: evidence types, opaque evidence references, and evidence groups
- `provenance.py`: knowledge origin and descriptive provenance records
- `classification.py`: descriptive classification contract models
- `query.py`: descriptive query intent contract models
- `store.py`: process-local exact identifier reference container

## Contract Separation

Classification and query modules define contracts only.

The classification contract describes supported categories and dimensions. It does not classify.

The query contract describes query intent. It does not execute, search, retrieve, filter, or rank.

## Runtime Reference Store

`KnowledgeReferenceStore` is an in-memory reference container. It keeps `UniversalKnowledge`
references in the current Python process and supports add, exact identifier get, exact identifier
remove, identifier enumeration, clear, statistics, and validation.

It is not a persistent store.

## Platform Integration Certification

The implemented Knowledge Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
classification contracts, query contracts, and the reference store.

## Relationship To Future Architecture

Future Context, Reasoning, Decision, and Agent layers may build above the Knowledge Foundation
after separate architecture approval. They are not implemented by this SDK.

Future persistent storage, query engines, search engines, graph systems, and reasoning systems are
also outside the implemented Knowledge Foundation.

## Constitutional Constraints

The Knowledge Foundation preserves these constraints:

- Knowledge remains platform-neutral.
- Evidence and provenance remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Classification, query execution, search, persistence, reasoning, AI, and workflow behavior remain
  out of scope.
