from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from packages.objects import LifecycleState, ValidationCategory, ValidationResult

from .core import UniversalExecution


@dataclass(frozen=True, slots=True)
class WorkspaceStatistics:
    total_executions: int
    active_executions: int
    archived_executions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total_executions": self.total_executions,
            "active_executions": self.active_executions,
            "archived_executions": self.archived_executions,
        }


class ExecutionWorkspace:
    """Process-local reference container for UniversalExecution objects."""

    def __init__(self) -> None:
        self._executions: dict[UUID, UniversalExecution] = {}

    def add(self, execution: UniversalExecution) -> None:
        result = validate_execution_reference(execution)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if execution.object_id in self._executions:
            raise ValueError(f"Execution reference already exists: {execution.object_id}")
        self._executions[execution.object_id] = execution

    def get(self, execution_id: UUID | str) -> UniversalExecution | None:
        return self._executions.get(_coerce_execution_id(execution_id))

    def remove(self, execution_id: UUID | str) -> UniversalExecution | None:
        return self._executions.pop(_coerce_execution_id(execution_id), None)

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._executions.keys(), key=str))

    def clear(self) -> None:
        self._executions.clear()

    def statistics(self) -> WorkspaceStatistics:
        active_count = sum(
            1
            for execution in self._executions.values()
            if isinstance(execution, UniversalExecution)
            and execution.lifecycle_state == LifecycleState.ACTIVE
        )
        archived_count = sum(
            1
            for execution in self._executions.values()
            if isinstance(execution, UniversalExecution)
            and execution.lifecycle_state == LifecycleState.ARCHIVED
        )
        return WorkspaceStatistics(
            total_executions=len(self._executions),
            active_executions=active_count,
            archived_executions=archived_count,
        )

    def validate(self) -> ValidationResult:
        return validate_execution_workspace(self)


def validate_execution_reference(execution: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(execution, UniversalExecution):
        result.add_error(
            "Execution workspace accepts only UniversalExecution instances.",
            ValidationCategory.SCHEMA,
            field="execution",
            code="invalid_execution_reference",
        )
        return result

    result.merge(execution.validate())
    return result


def validate_workspace_statistics(statistics: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(statistics, WorkspaceStatistics):
        result.add_error(
            "Workspace statistics must be a WorkspaceStatistics value.",
            ValidationCategory.METADATA,
            field="workspace_statistics",
            code="invalid_workspace_statistics",
        )
        return result

    if not isinstance(statistics.total_executions, int) or statistics.total_executions < 0:
        result.add_error(
            "Workspace total executions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.total_executions",
            code="invalid_workspace_total_executions",
        )

    if not isinstance(statistics.active_executions, int) or statistics.active_executions < 0:
        result.add_error(
            "Workspace active executions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.active_executions",
            code="invalid_workspace_active_executions",
        )

    if not isinstance(statistics.archived_executions, int) or statistics.archived_executions < 0:
        result.add_error(
            "Workspace archived executions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.archived_executions",
            code="invalid_workspace_archived_executions",
        )

    if (
        isinstance(statistics.total_executions, int)
        and isinstance(statistics.active_executions, int)
        and isinstance(statistics.archived_executions, int)
        and statistics.active_executions + statistics.archived_executions
        > statistics.total_executions
    ):
        result.add_error(
            "Workspace active and archived counts cannot exceed total executions.",
            ValidationCategory.METADATA,
            field="workspace_statistics",
            code="invalid_workspace_statistics_totals",
        )

    return result


def validate_execution_workspace(workspace: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(workspace, ExecutionWorkspace):
        result.add_error(
            "Workspace validation requires an ExecutionWorkspace instance.",
            ValidationCategory.SCHEMA,
            field="workspace",
            code="invalid_execution_workspace",
        )
        return result

    seen_ids: set[UUID] = set()
    for execution_id, execution in workspace._executions.items():
        if execution_id in seen_ids:
            result.add_error(
                "Execution reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="execution_id",
                code="duplicate_execution_reference",
            )
        seen_ids.add(execution_id)

        if not isinstance(execution, UniversalExecution):
            result.add_error(
                "Stored execution references must be UniversalExecution instances.",
                ValidationCategory.SCHEMA,
                field=str(execution_id),
                code="invalid_stored_execution_reference",
            )
        elif execution.object_id != execution_id:
            result.add_error(
                "Stored execution reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(execution_id),
                code="execution_reference_identity_mismatch",
            )
        else:
            result.merge(execution.validate())

    result.merge(validate_workspace_statistics(workspace.statistics()))
    return result


def _coerce_execution_id(execution_id: UUID | str) -> UUID:
    if isinstance(execution_id, UUID):
        return execution_id
    return UUID(execution_id)
