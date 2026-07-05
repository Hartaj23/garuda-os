# Action Foundation Architecture Guide

## Overview

The Universal Action Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0008. It builds on Platform Core and introduces Action objects, descriptive input and
provenance records, deterministic payloads, descriptive strategy and chain contracts, and a runtime
workspace.

## Relationship To Platform Core

`UniversalAction` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

The Action Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Action models may record memory-related identifiers through `ActionInputReference` values. These
identifiers are opaque. Action models do not hold `UniversalMemory` instances directly, and Memory
Foundation packages do not depend on Action Foundation packages.

## Relationship To Knowledge Foundation

Action models may record knowledge-related identifiers through `ActionInputReference` values. These
identifiers are opaque. Action models do not hold `UniversalKnowledge` instances directly, and
Knowledge Foundation packages do not depend on Action Foundation packages.

## Relationship To Context Foundation

Action models may record context-related identifiers through `ActionInputReference` values. These
identifiers are opaque. Action models do not hold `UniversalContext` instances directly, and Context
Foundation packages do not depend on Action Foundation packages.

## Relationship To Reasoning Foundation

Action models may record reasoning-related identifiers through `ActionInputReference` values. These
identifiers are opaque. Action models do not hold `UniversalReasoning` instances directly, and
Reasoning Foundation packages do not depend on Action Foundation packages.

## Relationship To Decision Foundation

Action models may record decision-related identifiers through `ActionInputReference` values. These
identifiers are opaque. Action models do not hold `UniversalDecision` instances directly, and
Decision Foundation packages do not depend on Action Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Action object, action type, state, outcome, confidence, metadata, validation
- `input.py`: opaque action input references and input collections
- `provenance.py`: descriptive action origin and provenance records
- `strategy.py`: descriptive strategy contract models
- `chain.py`: descriptive chain contract models
- `workspace.py`: process-local exact identifier Action workspace

## Contract Separation

Strategy and chain modules define contracts only.

The strategy contract describes strategy intent. It does not execute or evaluate strategies.

The chain contract describes chain structure over opaque step references. It does not execute,
resolve, search, orchestrate, optimize, schedule, or compute outcomes.

## Runtime Workspace

`ActionWorkspace` is a runtime reference container. It keeps `UniversalAction` references in the
current Python process and supports add, exact identifier get, exact identifier remove, identifier
enumeration, clear, statistics, and validation.

It is not a persistent store and is not serializable.

## Platform Integration Certification

The implemented Action Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
Knowledge Foundation coexistence, Context Foundation coexistence, Reasoning Foundation coexistence,
Decision Foundation coexistence, strategy contracts, chain contracts, and the workspace.

## Relationship To Future Architecture

Future workflow, orchestration, or Agent layers may build above the Action Foundation after separate
architecture approval. They are not implemented by this SDK.

Future action engines, strategy execution, chain execution, outcome computation, reference
resolution, provenance evaluation, scheduling, orchestration, optimization, persistent storage,
search, AI integration, REST APIs, frontend behavior, autonomous behavior, and workflow systems are
outside the implemented Action Foundation.

## Constitutional Constraints

The Action Foundation preserves these constraints:

- Actions remain platform-neutral.
- Inputs and provenance remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Action execution, outcome computation, scheduling, orchestration, search, persistence, AI, REST,
  frontend, autonomous behavior, and workflow behavior remain out of scope.
