from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .input import ActionInputCollection, validate_action_input_collection
from .provenance import ActionProvenance, validate_action_provenance


class ActionType(StrEnum):
    TASK = "task"
    REVIEW = "review"
    APPROVAL = "approval"
    NOTIFICATION = "notification"
    COMMAND = "command"
    OBSERVATION = "observation"


class ActionState(StrEnum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    READY = "ready"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ActionOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    DEFERRED = "deferred"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ActionConfidence:
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
class ActionMetadata:
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


class UniversalAction(CanonicalObject):
    """Platform-level action object."""

    def __init__(
        self,
        action_type: ActionType,
        action_state: ActionState = ActionState.DRAFT,
        action_outcome: ActionOutcome = ActionOutcome.UNKNOWN,
        action_confidence: ActionConfidence | None = None,
        action_metadata: ActionMetadata | None = None,
        action_inputs: ActionInputCollection | None = None,
        action_provenance: ActionProvenance | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._action_type = action_type
        self._action_state = action_state
        self._action_outcome = action_outcome
        self._action_confidence = action_confidence or ActionConfidence()
        self._action_metadata = action_metadata or ActionMetadata()
        self._action_inputs = action_inputs
        self._action_provenance = action_provenance
        self.register_validation_hook(validate_action)

    @property
    def action_type(self) -> ActionType:
        return self._action_type

    @property
    def action_state(self) -> ActionState:
        return self._action_state

    @property
    def action_outcome(self) -> ActionOutcome:
        return self._action_outcome

    @property
    def action_confidence(self) -> ActionConfidence:
        return self._action_confidence

    @property
    def action_metadata(self) -> ActionMetadata:
        return self._action_metadata

    @property
    def action_inputs(self) -> ActionInputCollection | None:
        return self._action_inputs

    @property
    def action_provenance(self) -> ActionProvenance | None:
        return self._action_provenance

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
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
            "action_type": self.action_type.value,
            "action_state": self.action_state.value,
            "action_outcome": self.action_outcome.value,
            "action_confidence": self.action_confidence.to_dict(),
            "action_metadata": self.action_metadata.to_dict(),
        }
        if self.action_inputs is not None:
            payload["action_inputs"] = self.action_inputs.to_dict()
        if self.action_provenance is not None:
            payload["action_provenance"] = self.action_provenance.to_dict()
        return payload


def validate_action(obj: UniversalAction) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "action_type", None), ActionType):
        result.add_error(
            "Action type must be an ActionType value.",
            ValidationCategory.SCHEMA,
            field="action_type",
            code="invalid_action_type",
        )

    if not isinstance(getattr(obj, "action_state", None), ActionState):
        result.add_error(
            "Action state must be an ActionState value.",
            ValidationCategory.LIFECYCLE,
            field="action_state",
            code="invalid_action_state",
        )

    if not isinstance(getattr(obj, "action_outcome", None), ActionOutcome):
        result.add_error(
            "Action outcome must be an ActionOutcome value.",
            ValidationCategory.METADATA,
            field="action_outcome",
            code="invalid_action_outcome",
        )

    if not isinstance(getattr(obj, "action_confidence", None), ActionConfidence):
        result.add_error(
            "Action confidence must be an ActionConfidence value.",
            ValidationCategory.METADATA,
            field="action_confidence",
            code="invalid_action_confidence",
        )

    if not isinstance(getattr(obj, "action_metadata", None), ActionMetadata):
        result.add_error(
            "Action metadata must be an ActionMetadata value.",
            ValidationCategory.METADATA,
            field="action_metadata",
            code="invalid_action_metadata",
        )

    action_inputs = getattr(obj, "action_inputs", None)
    if action_inputs is not None:
        result.merge(validate_action_input_collection(action_inputs))

    action_provenance = getattr(obj, "action_provenance", None)
    if action_provenance is not None:
        result.merge(validate_action_provenance(action_provenance))

    return result
