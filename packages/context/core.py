from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .scope import ContextScope, ContextScopeType
from .source import ContextSource, ContextSourceType


class ContextType(StrEnum):
    CONVERSATIONAL = "conversational"
    OPERATIONAL = "operational"
    ANALYTICAL = "analytical"
    ENVIRONMENTAL = "environmental"
    TEMPORAL = "temporal"


class ContextState(StrEnum):
    DRAFT = "draft"
    ASSEMBLED = "assembled"
    VALIDATED = "validated"
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class ContextConfidence:
    level: str = "unknown"
    rationale: str | None = None

    def __post_init__(self) -> None:
        if self.level not in {"unknown", "low", "medium", "high"}:
            raise ValueError("level must be one of: unknown, low, medium, high")

    def to_dict(self) -> dict[str, str | None]:
        return {
            "level": self.level,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class ContextMetadata:
    values: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.values, dict):
            object.__setattr__(self, "values", tuple(sorted(self.values.items())))
        elif isinstance(self.values, tuple):
            object.__setattr__(self, "values", tuple(sorted(self.values)))
        else:
            raise ValueError("values must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


class UniversalContext(CanonicalObject):
    """Platform-level context object."""

    def __init__(
        self,
        context_type: ContextType,
        context_state: ContextState = ContextState.DRAFT,
        context_confidence: ContextConfidence | None = None,
        context_metadata: ContextMetadata | None = None,
        context_source: ContextSource | None = None,
        context_scope: ContextScope | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._context_type = context_type
        self._context_state = context_state
        self._context_confidence = context_confidence or ContextConfidence()
        self._context_metadata = context_metadata or ContextMetadata()
        self._context_source = context_source
        self._context_scope = context_scope
        self.register_validation_hook(validate_context)

    @property
    def context_type(self) -> ContextType:
        return self._context_type

    @property
    def context_state(self) -> ContextState:
        return self._context_state

    @property
    def context_confidence(self) -> ContextConfidence:
        return self._context_confidence

    @property
    def context_metadata(self) -> ContextMetadata:
        return self._context_metadata

    @property
    def context_source(self) -> ContextSource | None:
        return self._context_source

    @property
    def context_scope(self) -> ContextScope | None:
        return self._context_scope

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "object_version": self.object_version,
            "object_type": self.object_type,
            "object_id": str(self.object_id),
            "metadata": dict(sorted(self.metadata.values.items())),
            "tags": list(self.tags),
            "lifecycle_state": self.lifecycle_state.value,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "context_type": self.context_type.value,
            "context_state": self.context_state.value,
            "context_confidence": self.context_confidence.to_dict(),
            "context_metadata": self.context_metadata.to_dict(),
            "context_source": self.context_source.to_dict() if self.context_source else None,
            "context_scope": self.context_scope.to_dict() if self.context_scope else None,
        }


def validate_context(obj: UniversalContext) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "context_type", None), ContextType):
        result.add_error(
            "Context type must be a ContextType value.",
            ValidationCategory.SCHEMA,
            field="context_type",
            code="invalid_context_type",
        )

    if not isinstance(getattr(obj, "context_state", None), ContextState):
        result.add_error(
            "Context state must be a ContextState value.",
            ValidationCategory.LIFECYCLE,
            field="context_state",
            code="invalid_context_state",
        )

    if not isinstance(getattr(obj, "context_confidence", None), ContextConfidence):
        result.add_error(
            "Context confidence must be a ContextConfidence value.",
            ValidationCategory.METADATA,
            field="context_confidence",
            code="invalid_context_confidence",
        )

    if not isinstance(getattr(obj, "context_metadata", None), ContextMetadata):
        result.add_error(
            "Context metadata must be a ContextMetadata value.",
            ValidationCategory.METADATA,
            field="context_metadata",
            code="invalid_context_metadata",
        )

    source = getattr(obj, "context_source", None)
    if source is not None:
        if not isinstance(source, ContextSource):
            result.add_error(
                "Context source must be a ContextSource value.",
                ValidationCategory.METADATA,
                field="context_source",
                code="invalid_context_source",
            )
        else:
            result.merge(validate_context_source(source))

    scope = getattr(obj, "context_scope", None)
    if scope is not None:
        if not isinstance(scope, ContextScope):
            result.add_error(
                "Context scope must be a ContextScope value.",
                ValidationCategory.METADATA,
                field="context_scope",
                code="invalid_context_scope",
            )
        else:
            result.merge(validate_context_scope(scope))

    return result


def validate_context_source(source: ContextSource) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(source.source_type, ContextSourceType):
        result.add_error(
            "Context source type must be a ContextSourceType value.",
            ValidationCategory.METADATA,
            field="context_source.source_type",
            code="invalid_context_source_type",
        )

    if not isinstance(source.source_identifier, str) or not source.source_identifier:
        result.add_error(
            "Context source identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="context_source.source_identifier",
            code="invalid_context_source_identifier",
        )

    if not hasattr(source.created_at, "isoformat"):
        result.add_error(
            "Context source creation timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="context_source.created_at",
            code="invalid_context_source_created_at",
        )

    if not isinstance(source.source_metadata, tuple):
        result.add_error(
            "Context source metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="context_source.source_metadata",
            code="invalid_context_source_metadata",
        )

    return result


def validate_context_scope(scope: ContextScope) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(scope.scope_type, ContextScopeType):
        result.add_error(
            "Context scope type must be a ContextScopeType value.",
            ValidationCategory.METADATA,
            field="context_scope.scope_type",
            code="invalid_context_scope_type",
        )

    if not isinstance(scope.boundary_identifier, str) or not scope.boundary_identifier:
        result.add_error(
            "Context scope boundary identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="context_scope.boundary_identifier",
            code="invalid_context_scope_boundary_identifier",
        )

    if not isinstance(scope.lifetime_metadata, tuple):
        result.add_error(
            "Context scope lifetime metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="context_scope.lifetime_metadata",
            code="invalid_context_scope_lifetime_metadata",
        )

    if not isinstance(scope.scope_metadata, tuple):
        result.add_error(
            "Context scope metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="context_scope.scope_metadata",
            code="invalid_context_scope_metadata",
        )

    return result
