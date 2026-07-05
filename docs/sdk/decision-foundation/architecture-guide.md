# Decision Foundation Architecture Guide

## Overview

The Universal Decision Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0007. It builds on Platform Core and introduces Decision objects, descriptive input and
provenance records, deterministic payloads, descriptive strategy and chain contracts, and a runtime
workspace.

## Relationship To Platform Core

`UniversalDecision` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

The Decision Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Decision models may record memory-related identifiers through `DecisionInputReference` values.
These identifiers are opaque. Decision models do not hold `UniversalMemory` instances directly, and
Memory Foundation packages do not depend on Decision Foundation packages.

## Relationship To Knowledge Foundation

Decision models may record knowledge-related identifiers through `DecisionInputReference` values.
These identifiers are opaque. Decision models do not hold `UniversalKnowledge` instances directly,
and Knowledge Foundation packages do not depend on Decision Foundation packages.

## Relationship To Context Foundation

Decision models may record context-related identifiers through `DecisionInputReference` values.
These identifiers are opaque. Decision models do not hold `UniversalContext` instances directly, and
Context Foundation packages do not depend on Decision Foundation packages.

## Relationship To Reasoning Foundation

Decision models may record reasoning-related identifiers through `DecisionInputReference` values.
These identifiers are opaque. Decision models do not hold `UniversalReasoning` instances directly,
and Reasoning Foundation packages do not depend on Decision Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Decision object, decision type, state, outcome, confidence, metadata,
  validation
- `input.py`: opaque decision input references and input collections
- `provenance.py`: descriptive decision origin and provenance records
- `strategy.py`: descriptive strategy contract models
- `chain.py`: descriptive chain contract models
- `workspace.py`: process-local exact identifier Decision workspace

## Contract Separation

Strategy and chain modules define contracts only.

The strategy contract describes strategy intent. It does not execute or evaluate strategies.

The chain contract describes chain structure over opaque step references. It does not execute,
resolve, search, orchestrate, optimize, or compute outcomes.

## Runtime Workspace

`DecisionWorkspace` is a runtime reference container. It keeps `UniversalDecision` references in the
current Python process and supports add, exact identifier get, exact identifier remove, identifier
enumeration, clear, statistics, and validation.

It is not a persistent store and is not serializable.

## Platform Integration Certification

The implemented Decision Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
Knowledge Foundation coexistence, Context Foundation coexistence, Reasoning Foundation coexistence,
strategy contracts, chain contracts, and the workspace.

## Relationship To Future Architecture

Future Agent and workflow layers may build above the Decision Foundation after separate architecture
approval. They are not implemented by this SDK.

Future decision engines, strategy execution, chain execution, outcome computation, reference
resolution, provenance evaluation, orchestration, planning, optimization, persistent storage,
search, AI integration, REST APIs, frontend behavior, autonomous behavior, and workflow systems are
outside the implemented Decision Foundation.

## Constitutional Constraints

The Decision Foundation preserves these constraints:

- Decisions remain platform-neutral.
- Inputs and provenance remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Decision execution, outcome computation, orchestration, search, persistence, AI, REST, frontend,
  autonomous behavior, and workflow behavior remain out of scope.
