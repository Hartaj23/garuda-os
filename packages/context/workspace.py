from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from packages.objects import ValidationCategory, ValidationResult

from .core import UniversalContext


@dataclass(frozen=True, slots=True)
class WorkspaceStatistics:
    total_contexts: int
    created_at: datetime
    last_modified_at: datetime

    def to_dict(self) -> dict[str, object]:
        return {
            "total_contexts": self.total_contexts,
            "created_at": self.created_at.isoformat(),
            "last_modified_at": self.last_modified_at.isoformat(),
        }


class ContextWorkspace:
    """Process-local reference container for UniversalContext objects."""

    def __init__(self) -> None:
        now = datetime.now(tz=UTC)
        self._contexts: dict[UUID, UniversalContext] = {}
        self._created_at = now
        self._last_modified_at = now

    def add(self, context: UniversalContext) -> None:
        result = validate_context_reference(context)
        if not result.is_valid:
            raise ValueError(result.errors[0].message)
        if context.object_id in self._contexts:
            raise ValueError(f"Context reference already exists: {context.object_id}")
        self._contexts[context.object_id] = context
        self._touch()

    def get(self, context_id: UUID | str) -> UniversalContext | None:
        return self._contexts.get(_coerce_context_id(context_id))

    def remove(self, context_id: UUID | str) -> UniversalContext | None:
        context = self._contexts.pop(_coerce_context_id(context_id), None)
        if context is not None:
            self._touch()
        return context

    def identifiers(self) -> tuple[UUID, ...]:
        return tuple(sorted(self._contexts.keys(), key=str))

    def clear(self) -> None:
        if self._contexts:
            self._contexts.clear()
            self._touch()

    def statistics(self) -> WorkspaceStatistics:
        return WorkspaceStatistics(
            total_contexts=len(self._contexts),
            created_at=self._created_at,
            last_modified_at=self._last_modified_at,
        )

    def validate(self) -> ValidationResult:
        return validate_context_workspace(self)

    def _touch(self) -> None:
        self._last_modified_at = datetime.now(tz=UTC)


def validate_context_reference(context: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(context, UniversalContext):
        result.add_error(
            "Context workspace accepts only UniversalContext instances.",
            ValidationCategory.SCHEMA,
            field="context",
            code="invalid_context_reference",
        )
        return result

    result.merge(context.validate())
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

    if not isinstance(statistics.total_contexts, int) or statistics.total_contexts < 0:
        result.add_error(
            "Workspace total contexts must be a non-negative integer.",
            ValidationCategory.METADATA,
            field="workspace_statistics.total_contexts",
            code="invalid_workspace_total_contexts",
        )

    if not hasattr(statistics.created_at, "isoformat"):
        result.add_error(
            "Workspace creation timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="workspace_statistics.created_at",
            code="invalid_workspace_created_at",
        )

    if not hasattr(statistics.last_modified_at, "isoformat"):
        result.add_error(
            "Workspace modification timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="workspace_statistics.last_modified_at",
            code="invalid_workspace_last_modified_at",
        )

    return result


def validate_context_workspace(workspace: object) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(workspace, ContextWorkspace):
        result.add_error(
            "Workspace validation requires a ContextWorkspace instance.",
            ValidationCategory.SCHEMA,
            field="workspace",
            code="invalid_context_workspace",
        )
        return result

    seen_ids: set[UUID] = set()
    for context_id, context in workspace._contexts.items():
        if context_id in seen_ids:
            result.add_error(
                "Context reference identifiers must be unique.",
                ValidationCategory.IDENTITY,
                field="context_id",
                code="duplicate_context_reference",
            )
        seen_ids.add(context_id)

        if not isinstance(context, UniversalContext):
            result.add_error(
                "Stored context references must be UniversalContext instances.",
                ValidationCategory.SCHEMA,
                field=str(context_id),
                code="invalid_stored_context_reference",
            )
        elif context.object_id != context_id:
            result.add_error(
                "Stored context reference key must match object identity.",
                ValidationCategory.IDENTITY,
                field=str(context_id),
                code="context_reference_identity_mismatch",
            )
        else:
            result.merge(context.validate())

    result.merge(validate_workspace_statistics(workspace.statistics()))
    return result


def _coerce_context_id(context_id: UUID | str) -> UUID:
    if isinstance(context_id, UUID):
        return context_id
    return UUID(context_id)
