# Memory Foundation Architecture Guide

## Overview

The Memory Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0003. It builds on Platform Core and introduces memory objects, provenance records,
deterministic memory payloads, descriptive contracts, and a runtime reference store.

## Relationship To Platform Core

`UniversalMemory` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage,
and serialization compatibility for inherited fields.

The Memory Foundation does not modify Platform Core packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Memory object, memory types, confidence, metadata, validation
- `source.py`: source and acquisition enums plus `MemorySource`
- `provenance.py`: provenance references, provenance metadata, and `MemoryProvenance`
- `index.py`: descriptive index contract models
- `retrieval.py`: descriptive retrieval request and response contract models
- `store.py`: process-local exact identifier reference container

## Contract Separation

Index and retrieval modules define contracts only.

The index contract describes what may be indexed by future systems. It does not index.

The retrieval contract describes request and response shape. It does not retrieve.

## Runtime Reference Store

`MemoryReferenceStore` is an in-memory reference container. It keeps `UniversalMemory` references in
the current Python process and supports add, exact identifier get, exact identifier remove,
identifier enumeration, clear, statistics, and validation.

It is not a persistent store.

## Relationship To Future Architecture

Future Knowledge, Context, Reasoning, Decision, and Agent layers may build above Memory Foundation
after separate architecture approval. They are not implemented by this SDK.

Future persistent storage, retrieval engines, search engines, vector stores, and knowledge systems
are also outside the implemented Memory Foundation.

## Constitutional Constraints

The Memory Foundation preserves these constraints:

- memory remains platform-neutral
- provenance remains explicit and deterministic
- contracts remain separate from implementations
- Platform Core remains the source of object identity and validation contracts
- storage, retrieval, search, AI, and workflow behavior remain out of scope
