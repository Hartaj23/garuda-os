from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from packages.objects import LifecycleState, ValidationCategory, ValidationResult

from .core import UniversalDecision


@dataclass(frozen=True, slots=True)
class WorkspaceStatistics:
    total_decisions: int
    active_decisions: int
    archived_decisions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total_decisions": self.total_decisions,
            "active_decisions": self.active_decisions,
            "archived_decisions": self.archived_decisions,
        }


class DecisionWorkspace:
    """Process-local reference container for UniversalDecision objects."""

    def __init__(self) -> None:
        self._decisions: dict[UUID, UniversalDecision] = {}

    def add(self, decision: UniversalDecision) -> None:
        result = validate_decision_reference(decision)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if decision.object_id in self._decisions:
            raise ValueError(f"Decision reference already exists: {decision.object_id}")
        self._decisions[decision.object_id] = decision

    def get(self, decision_id: UUID | str) -> UniversalDecision | None:
        return self._decisions.get(_coerce_decision_id(decision_id))

    def remove(self, decision_id: UUID | str) -> UniversalDecision | None:
        return self._decisions.pop(_coerce_decision_id(decision_id), None)

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._decisions.keys(), key=str))

    def clear(self) -> None:
        self._decisions.clear()

    def statistics(self) -> WorkspaceStatistics:
        active_count = sum(
            1
            for decision in self._decisions.values()
            if isinstance(decision, UniversalDecision)
            and decision.lifecycle_state == LifecycleState.ACTIVE
        )
        archived_count = sum(
            1
            for decision in self._decisions.values()
            if isinstance(decision, UniversalDecision)
            and decision.lifecycle_state == LifecycleState.ARCHIVED
        )
        return WorkspaceStatistics(
            total_decisions=len(self._decisions),
            active_decisions=active_count,
            archived_decisions=archived_count,
        )

    def validate(self) -> ValidationResult:
        return validate_decision_workspace(self)


def validate_decision_reference(decision: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(decision, UniversalDecision):
        result.add_error(
            "Decision workspace accepts only UniversalDecision instances.",
            ValidationCategory.SCHEMA,
            field="decision",
            code="invalid_decision_reference",
        )
        return result

    result.merge(decision.validate())
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

    if not isinstance(statistics.total_decisions, int) or statistics.total_decisions < 0:
        result.add_error(
            "Workspace total decisions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.total_decisions",
            code="invalid_workspace_total_decisions",
        )

    if not isinstance(statistics.active_decisions, int) or statistics.active_decisions < 0:
        result.add_error(
            "Workspace active decisions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.active_decisions",
            code="invalid_workspace_active_decisions",
        )

    if (
        not isinstance(statistics.archived_decisions, int)
        or statistics.archived_decisions < 0
    ):
        result.add_error(
            "Workspace archived decisions must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.archived_decisions",
            code="invalid_workspace_archived_decisions",
        )

    if (
        isinstance(statistics.total_decisions, int)
        and isinstance(statistics.active_decisions, int)
        and isinstance(statistics.archived_decisions, int)
        and statistics.active_decisions + statistics.archived_decisions
        > statistics.total_decisions
    ):
        result.add_error(
            "Workspace active and archived counts cannot exceed total decisions.",
            ValidationCategory.METADATA,
            field="workspace_statistics",
            code="invalid_workspace_statistics_totals",
        )

    return result


def validate_decision_workspace(workspace: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(workspace, DecisionWorkspace):
        result.add_error(
            "Workspace validation requires a DecisionWorkspace instance.",
            ValidationCategory.SCHEMA,
            field="workspace",
            code="invalid_decision_workspace",
        )
        return result

    seen_ids: set[UUID] = set()
    for decision_id, decision in workspace._decisions.items():
        if decision_id in seen_ids:
            result.add_error(
                "Decision reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="decision_id",
                code="duplicate_decision_reference",
            )
        seen_ids.add(decision_id)

        if not isinstance(decision, UniversalDecision):
            result.add_error(
                "Stored decision references must be UniversalDecision instances.",
                ValidationCategory.SCHEMA,
                field=str(decision_id),
                code="invalid_stored_decision_reference",
            )
        elif decision.object_id != decision_id:
            result.add_error(
                "Stored decision reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(decision_id),
                code="decision_reference_identity_mismatch",
            )
        else:
            result.merge(decision.validate())

    result.merge(validate_workspace_statistics(workspace.statistics()))
    return result


def _coerce_decision_id(decision_id: UUID | str) -> UUID:
    if isinstance(decision_id, UUID):
        return decision_id
    return UUID(decision_id)
