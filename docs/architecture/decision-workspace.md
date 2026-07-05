# Decision Workspace

## Purpose

The Decision Workspace is the GAR-SPRINT-0007 Mission Foxtrot runtime container for
`UniversalDecision` references.

It is process-local and runtime-only. It stores `UniversalDecision` objects by exact platform
identifier and preserves object identity. It does not execute decisions, compute outcomes,
orchestrate decision behavior, search, retrieve by criteria, rank, persist records or perform AI
behavior.

## Package Structure

The implementation lives in `packages/decision/workspace.py` and is exported from
`packages/decision/__init__.py`.

The module defines:

- `WorkspaceStatistics`
- `DecisionWorkspace`
- `validate_decision_reference`
- `validate_decision_workspace`
- `validate_workspace_statistics`

## Workspace Model

`DecisionWorkspace` is a mutable process-local container. It supports only exact identifier
operations:

- add a `UniversalDecision` object
- get a `UniversalDecision` object by `UUID` or UUID string
- remove a `UniversalDecision` object by `UUID` or UUID string
- enumerate stored identifiers deterministically
- clear the workspace
- return deterministic descriptive statistics

The workspace rejects duplicate identifiers and non-`UniversalDecision` objects. The workspace
itself intentionally has no `to_dict()` method and is not serializable.

## Statistics Model

`WorkspaceStatistics` is an immutable value model with deterministic payloads:

- `total_decisions`
- `active_decisions`
- `archived_decisions`

The active and archived counts are derived from the Platform Core lifecycle state of stored
`UniversalDecision` objects. Statistics are descriptive only.

## Validation Model

Mission Foxtrot reuses Platform Core validation primitives through `ValidationResult` and
`ValidationCategory`.

Local validation helpers verify:

- workspace shape
- stored decision object type
- stored identifier consistency
- `WorkspaceStatistics` structure

No validation engine is introduced.

## Dependency Boundaries

The Decision Workspace depends only on Platform Core validation and lifecycle primitives and the
existing `UniversalDecision` object. It does not modify Platform Core, Memory Foundation, Knowledge
Foundation, Context Foundation or Reasoning Foundation.

## Explicit Exclusions

The Decision Workspace does not implement:

- Decision execution
- Outcome computation
- Decision orchestration
- Decision optimization
- Reference resolution
- Criteria retrieval
- Search
- Ranking
- Persistence
- AI behavior
- REST APIs
- Frontend behavior
- Workflow behavior
