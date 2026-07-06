# Execution Foundation Architecture Guide

## Overview

The Universal Execution Foundation is a service-independent platform subsystem implemented during
GAR-SPRINT-0009. It builds on Platform Core and introduces Execution objects, descriptive input and
provenance records, deterministic payloads, descriptive strategy and chain contracts, and a runtime
workspace.

## Relationship To Platform Core

`UniversalExecution` inherits from Platform Core `CanonicalObject`. It reuses Platform Core object
identity, metadata, tags, lifecycle state, audit fields, validation hooks, relationship storage, and
serialization compatibility for inherited fields.

The Execution Foundation does not modify Platform Core packages.

## Relationship To Memory Foundation

Execution models may record memory-related identifiers through `ExecutionInputReference` values.
These identifiers are opaque. Execution models do not hold `UniversalMemory` instances directly, and
Memory Foundation packages do not depend on Execution Foundation packages.

## Relationship To Knowledge Foundation

Execution models may record knowledge-related identifiers through `ExecutionInputReference` values.
These identifiers are opaque. Execution models do not hold `UniversalKnowledge` instances directly, and
Knowledge Foundation packages do not depend on Execution Foundation packages.

## Relationship To Context Foundation

Execution models may record context-related identifiers through `ExecutionInputReference` values.
These identifiers are opaque. Execution models do not hold `UniversalContext` instances directly, and
Context Foundation packages do not depend on Execution Foundation packages.

## Relationship To Reasoning Foundation

Execution models may record reasoning-related identifiers through `ExecutionInputReference` values.
These identifiers are opaque. Execution models do not hold `UniversalReasoning` instances directly, and
Reasoning Foundation packages do not depend on Execution Foundation packages.

## Relationship To Decision Foundation

Execution models may record decision-related identifiers through `ExecutionInputReference` values.
These identifiers are opaque. Execution models do not hold `UniversalDecision` instances directly, and
Decision Foundation packages do not depend on Execution Foundation packages.

## Relationship To Action Foundation

Execution models may record action-related identifiers through `ExecutionInputReference` values. These
identifiers are opaque. Execution models do not hold `UniversalAction` instances directly, and Action
Foundation packages do not depend on Execution Foundation packages.

## Layer Boundaries

The implemented layers are:

- `core.py`: Universal Execution object, execution type, state, outcome, confidence, metadata, validation
- `input.py`: opaque execution input references and input collections
- `provenance.py`: descriptive execution origin and provenance records
- `strategy.py`: descriptive strategy contract models
- `chain.py`: descriptive chain contract models
- `workspace.py`: process-local exact identifier Execution workspace

## Contract Separation

Strategy and chain modules define contracts only.

The strategy contract describes strategy intent. It does not execute or evaluate strategies.

The chain contract describes chain structure over opaque step references. It does not execute,
resolve, search, orchestrate, optimize, schedule, or compute outcomes.

## Runtime Workspace

`ExecutionWorkspace` is a runtime reference container. It keeps `UniversalExecution` references in the
current Python process and supports add, exact identifier get, exact identifier remove, identifier
enumeration, clear, statistics, and validation.

It is not a persistent store and is not serializable.

## Platform Integration Certification

The implemented Execution Foundation has certification tests covering Platform Core inheritance,
validation, deterministic payloads, Platform Core serialization compatibility, registry
compatibility, lifecycle compatibility, relationship compatibility, Memory Foundation coexistence,
Knowledge Foundation coexistence, Context Foundation coexistence, Reasoning Foundation coexistence,
Decision Foundation coexistence, Action Foundation coexistence, strategy contracts, chain contracts,
and the workspace.

## Relationship To Future Architecture

Future workflow, orchestration, or Agent layers may build above the Execution Foundation after
separate architecture approval. They are not implemented by this SDK.

Future execution engines, strategy execution, chain execution, outcome computation, reference
resolution, provenance evaluation, scheduling, orchestration, optimization, persistent storage,
search, AI integration, REST APIs, frontend behavior, autonomous behavior, and workflow systems are
outside the implemented Execution Foundation.

## Constitutional Constraints

The Execution Foundation preserves these constraints:

- Executions remain platform-neutral.
- Inputs and provenance remain explicit and deterministic.
- Contracts remain separate from implementations.
- Platform Core remains the source of object identity and validation contracts.
- Execution behavior, outcome computation, scheduling, orchestration, search, persistence, AI, REST,
  frontend, autonomous behavior, and workflow behavior remain out of scope.
