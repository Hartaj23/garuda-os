from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from packages.objects import LifecycleState, ValidationCategory, ValidationResult

from .core import UniversalAction


@dataclass(frozen=True, slots=True)
class WorkspaceStatistics:
    total_actions: int
    active_actions: int
    archived_actions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total_actions": self.total_actions,
            "active_actions": self.active_actions,
            "archived_actions": self.archived_actions,
        }


class ActionWorkspace:
    """Process-local reference container for UniversalAction objects."""

    def __init__(self) -> None:
        self._actions: dict[UUID, UniversalAction] = {}

    def add(self, action: UniversalAction) -> None:
        result = validate_action_reference(action)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if action.object_id in self._actions:
            raise ValueError(f"Action reference already exists: {action.object_id}")
        self._actions[action.object_id] = action

    def get(self, action_id: UUID | str) -> UniversalAction | None:
        return self._actions.get(_coerce_action_id(action_id))

    def remove(self, action_id: UUID | str) -> UniversalAction | None:
        return self._actions.pop(_coerce_action_id(action_id), None)

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._actions.keys(), key=str))

    def clear(self) -> None:
        self._actions.clear()

    def statistics(self) -> WorkspaceStatistics:
        active_count = sum(
            1
            for action in self._actions.values()
            if isinstance(action, UniversalAction)
            and action.lifecycle_state == LifecycleState.ACTIVE
        )
        archived_count = sum(
            1
            for action in self._actions.values()
            if isinstance(action, UniversalAction)
            and action.lifecycle_state == LifecycleState.ARCHIVED
        )
        return WorkspaceStatistics(
            total_actions=len(self._actions),
            active_actions=active_count,
            archived_actions=archived_count,
        )

    def validate(self) -> ValidationResult:
        return validate_action_workspace(self)


def validate_action_reference(action: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(action, UniversalAction):
        result.add_error(
            "Action workspace accepts only UniversalAction instances.",
            ValidationCategory.SCHEMA,
            field="action",
            code="invalid_action_reference",
        )
        return result

    result.merge(action.validate())
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

    if not isinstance(statistics.total_actions, int) or statistics.total_actions < 0:
        result.add_error(
            "Workspace total actions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.total_actions",
            code="invalid_workspace_total_actions",
        )

    if not isinstance(statistics.active_actions, int) or statistics.active_actions < 0:
        result.add_error(
            "Workspace active actions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.active_actions",
            code="invalid_workspace_active_actions",
        )

    if not isinstance(statistics.archived_actions, int) or statistics.archived_actions < 0:
        result.add_error(
            "Workspace archived actions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.archived_actions",
            code="invalid_workspace_archived_actions",
        )

    if (
        isinstance(statistics.total_actions, int)
        and isinstance(statistics.active_actions, int)
        and isinstance(statistics.archived_actions, int)
        and statistics.active_actions + statistics.archived_actions
        > statistics.total_actions
    ):
        result.add_error(
            "Workspace active and archived counts cannot exceed total actions.",
            ValidationCategory.METADATA,
            field="workspace_statistics",
            code="invalid_workspace_statistics_totals",
        )

    return result


def validate_action_workspace(workspace: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(workspace, ActionWorkspace):
        result.add_error(
            "Workspace validation requires an ActionWorkspace instance.",
            ValidationCategory.SCHEMA,
            field="workspace",
            code="invalid_action_workspace",
        )
        return result

    seen_ids: set[UUID] = set()
    for action_id, action in workspace._actions.items():
        if action_id in seen_ids:
            result.add_error(
                "Action reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="action_id",
                code="duplicate_action_reference",
            )
        seen_ids.add(action_id)

        if not isinstance(action, UniversalAction):
            result.add_error(
                "Stored action references must be UniversalAction instances.",
                ValidationCategory.SCHEMA,
                field=str(action_id),
                code="invalid_stored_action_reference",
            )
        elif action.object_id != action_id:
            result.add_error(
                "Stored action reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(action_id),
                code="action_reference_identity_mismatch",
            )
        else:
            result.merge(action.validate())

    result.merge(validate_workspace_statistics(workspace.statistics()))
    return result


def _coerce_action_id(action_id: UUID | str) -> UUID:
    if isinstance(action_id, UUID):
        return action_id
    return UUID(action_id)
