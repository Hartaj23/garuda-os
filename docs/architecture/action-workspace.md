# Action Workspace

## Purpose

The Action Workspace is the GAR-SPRINT-0008 Mission Foxtrot runtime container for
`UniversalAction` references.

It is process-local and runtime-only. It stores `UniversalAction` objects by exact platform
identifier and preserves object identity. It does not execute actions, schedule actions,
orchestrate workflows, search, retrieve by criteria, rank, persist records or perform AI behavior.

## Package Structure

The implementation lives in `packages/action/workspace.py` and is exported from
`packages/action/__init__.py`.

The module defines:

- `WorkspaceStatistics`
- `ActionWorkspace`
- `validate_action_reference`
- `validate_action_workspace`
- `validate_workspace_statistics`

## Workspace Model

`ActionWorkspace` is a mutable process-local container. It supports only exact identifier
operations:

- add a `UniversalAction` object
- get a `UniversalAction` object by `UUID` or UUID string
- remove a `UniversalAction` object by `UUID` or UUID string
- enumerate stored identifiers deterministically
- clear the workspace
- return deterministic descriptive statistics

The workspace rejects duplicate identifiers and non-`UniversalAction` objects. The workspace itself
intentionally has no `to_dict()` method and is not serializable.

## Statistics Model

`WorkspaceStatistics` is an immutable value model with deterministic payloads:

- `total_actions`
- `active_actions`
- `archived_actions`

The active and archived counts are derived from the Platform Core lifecycle state of stored
`UniversalAction` objects. Statistics are descriptive only.

## Validation Model

Mission Foxtrot reuses Platform Core validation primitives through `ValidationResult` and
`ValidationCategory`.

Local validation helpers verify:

- workspace shape
- stored action object type
- stored identifier consistency
- `WorkspaceStatistics` structure

No validation engine is introduced.

## Dependency Boundaries

The Action Workspace depends only on Platform Core validation and lifecycle primitives and the
existing `UniversalAction` object. It does not modify Platform Core, Memory Foundation, Knowledge
Foundation, Context Foundation, Reasoning Foundation or Decision Foundation.

## Explicit Exclusions

The Action Workspace does not implement:

- Action execution
- Outcome computation
- Action scheduling
- Workflow orchestration
- Action optimization
- Reference resolution
- Criteria retrieval
- Search
- Ranking
- Persistence
- AI behavior
- REST APIs
- Frontend behavior
- Autonomous behavior
