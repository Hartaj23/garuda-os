# Reasoning Foundation Architecture Guide

## Overview

The Universal Reasoning Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0006. It builds on Platform Core and introduces Reasoning objects, descriptive input and
provenance records, deterministic payloads, descriptive strategy and chain contracts, and a runtime
workspace.

## Relationship To Platform Core

`UniversalReasoning` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage,
and serialization compatibility for inherited fields.

The Reasoning Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Reasoning models may record memory-related identifiers through `ReasoningInputReference` values.
These identifiers are opaque. Reasoning models do not hold `UniversalMemory` instances directly,
and Memory Foundation packages do not depend on Reasoning Foundation packages.

## Relationship To Knowledge Foundation

Reasoning models may record knowledge-related identifiers through `ReasoningInputReference` values.
These identifiers are opaque. Reasoning models do not hold `UniversalKnowledge` instances directly,
and Knowledge Foundation packages do not depend on Reasoning Foundation packages.

## Relationship To Context Foundation

Reasoning models may record context-related identifiers through `ReasoningInputReference` values.
These identifiers are opaque. Reasoning models do not hold `UniversalContext` instances directly,
and Context Foundation packages do not depend on Reasoning Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Reasoning object, reasoning type, state, confidence, metadata, validation
- `input.py`: opaque reasoning input references and input collections
- `provenance.py`: descriptive reasoning origin and provenance records
- `strategy.py`: descriptive strategy contract models
- `chain.py`: descriptive chain contract models
- `workspace.py`: process-local exact identifier Reasoning workspace

## Contract Separation

Strategy and chain modules define contracts only.

The strategy contract describes strategy intent. It does not execute or evaluate strategies.

The chain contract describes chain structure over opaque step references. It does not execute,
resolve, search, infer, or generate conclusions.

## Runtime Workspace

`ReasoningWorkspace` is a runtime reference container. It keeps `UniversalReasoning` references in
the current Python process and supports add, exact identifier get, exact identifier remove,
identifier enumeration, clear, statistics, and validation.

It is not a persistent store and is not serializable.

## Platform Integration Certification

The implemented Reasoning Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
Knowledge Foundation coexistence, Context Foundation coexistence, strategy contracts, chain
contracts, and the workspace.

## Relationship To Future Architecture

Future Decision and Agent layers may build above the Reasoning Foundation after separate
architecture approval. They are not implemented by this SDK.

Future reasoning engines, inference engines, strategy execution, chain execution, conclusion
generation, planning, decision making, orchestration, persistent storage, search, AI integration,
REST APIs, frontend behavior, and workflow systems are outside the implemented Reasoning
Foundation.

## Constitutional Constraints

The Reasoning Foundation preserves these constraints:

- Reasoning remains platform-neutral.
- Inputs and provenance remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Reasoning execution, inference, conclusion generation, search, persistence, AI, REST, frontend,
  and workflow behavior remain out of scope.
