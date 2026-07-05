from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from packages.objects import LifecycleState, ValidationCategory, ValidationResult

from .core import UniversalReasoning


@dataclass(frozen=True, slots=True)
class WorkspaceStatistics:
    total_reasoning_objects: int
    active_reasoning_objects: int
    archived_reasoning_objects: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total_reasoning_objects": self.total_reasoning_objects,
            "active_reasoning_objects": self.active_reasoning_objects,
            "archived_reasoning_objects": self.archived_reasoning_objects,
        }


class ReasoningWorkspace:
    """Process-local reference container for UniversalReasoning objects."""

    def __init__(self) -> None:
        self._reasoning_objects: dict[UUID, UniversalReasoning] = {}

    def add(self, reasoning: UniversalReasoning) -> None:
        result = validate_reasoning_reference(reasoning)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if reasoning.object_id in self._reasoning_objects:
            raise ValueError(f"Reasoning reference already exists: {reasoning.object_id}")
        self._reasoning_objects[reasoning.object_id] = reasoning

    def get(self, reasoning_id: UUID | str) -> UniversalReasoning | None:
        return self._reasoning_objects.get(_coerce_reasoning_id(reasoning_id))

    def remove(self, reasoning_id: UUID | str) -> UniversalReasoning | None:
        return self._reasoning_objects.pop(_coerce_reasoning_id(reasoning_id), None)

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._reasoning_objects.keys(), key=str))

    def clear(self) -> None:
        self._reasoning_objects.clear()

    def statistics(self) -> WorkspaceStatistics:
        active_count = sum(
            1
            for reasoning in self._reasoning_objects.values()
            if isinstance(reasoning, UniversalReasoning)
            and reasoning.lifecycle_state == LifecycleState.ACTIVE
        )
        archived_count = sum(
            1
            for reasoning in self._reasoning_objects.values()
            if isinstance(reasoning, UniversalReasoning)
            and reasoning.lifecycle_state == LifecycleState.ARCHIVED
        )
        return WorkspaceStatistics(
            total_reasoning_objects=len(self._reasoning_objects),
            active_reasoning_objects=active_count,
            archived_reasoning_objects=archived_count,
        )

    def validate(self) -> ValidationResult:
        return validate_reasoning_workspace(self)


def validate_reasoning_reference(reasoning: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reasoning, UniversalReasoning):
        result.add_error(
            "Reasoning workspace accepts only UniversalReasoning instances.",
            ValidationCategory.SCHEMA,
            field="reasoning",
            code="invalid_reasoning_reference",
        )
        return result

    result.merge(reasoning.validate())
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

    if (
        not isinstance(statistics.total_reasoning_objects, int)
        or statistics.total_reasoning_objects < 0
    ):
        result.add_error(
            "Workspace total reasoning objects must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.total_reasoning_objects",
            code="invalid_workspace_total_reasoning_objects",
        )

    if (
        not isinstance(statistics.active_reasoning_objects, int)
        or statistics.active_reasoning_objects < 0
    ):
        result.add_error(
            "Workspace active reasoning objects must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.active_reasoning_objects",
            code="invalid_workspace_active_reasoning_objects",
        )

    if (
        not isinstance(statistics.archived_reasoning_objects, int)
        or statistics.archived_reasoning_objects < 0
    ):
        result.add_error(
            "Workspace archived reasoning objects must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.archived_reasoning_objects",
            code="invalid_workspace_archived_reasoning_objects",
        )

    if (
        isinstance(statistics.total_reasoning_objects, int)
        and isinstance(statistics.active_reasoning_objects, int)
        and isinstance(statistics.archived_reasoning_objects, int)
        and statistics.active_reasoning_objects + statistics.archived_reasoning_objects
        > statistics.total_reasoning_objects
    ):
        result.add_error(
            "Workspace active and archived counts cannot exceed total reasoning objects.",
            ValidationCategory.METADATA,
            field="workspace_statistics",
            code="invalid_workspace_statistics_totals",
        )

    return result


def validate_reasoning_workspace(workspace: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(workspace, ReasoningWorkspace):
        result.add_error(
            "Workspace validation requires a ReasoningWorkspace instance.",
            ValidationCategory.SCHEMA,
            field="workspace",
            code="invalid_reasoning_workspace",
        )
        return result

    seen_ids: set[UUID] = set()
    for reasoning_id, reasoning in workspace._reasoning_objects.items():
        if reasoning_id in seen_ids:
            result.add_error(
                "Reasoning reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="reasoning_id",
                code="duplicate_reasoning_reference",
            )
        seen_ids.add(reasoning_id)

        if not isinstance(reasoning, UniversalReasoning):
            result.add_error(
                "Stored reasoning references must be UniversalReasoning instances.",
                ValidationCategory.SCHEMA,
                field=str(reasoning_id),
                code="invalid_stored_reasoning_reference",
            )
        elif reasoning.object_id != reasoning_id:
            result.add_error(
                "Stored reasoning reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(reasoning_id),
                code="reasoning_reference_identity_mismatch",
            )
        else:
            result.merge(reasoning.validate())

    result.merge(validate_workspace_statistics(workspace.statistics()))
    return result


def _coerce_reasoning_id(reasoning_id: UUID | str) -> UUID:
    if isinstance(reasoning_id, UUID):
        return reasoning_id
    return UUID(reasoning_id)
