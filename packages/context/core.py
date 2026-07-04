from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult


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
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._context_type = context_type
        self._context_state = context_state
        self._context_confidence = context_confidence or ContextConfidence()
        self._context_metadata = context_metadata or ContextMetadata()
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

    return result
