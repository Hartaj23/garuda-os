from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .input import DecisionInputCollection, validate_decision_input_collection
from .provenance import DecisionProvenance, validate_decision_provenance


class DecisionType(StrEnum):
    RECOMMENDATION = "recommendation"
    SELECTION = "selection"
    APPROVAL = "approval"
    REJECTION = "rejection"
    DEFERMENT = "deferment"
    OBSERVATION = "observation"


class DecisionState(StrEnum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    ARCHIVED = "archived"


class DecisionOutcome(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DecisionConfidence:
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
class DecisionMetadata:
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


class UniversalDecision(CanonicalObject):
    """Platform-level decision object."""

    def __init__(
        self,
        decision_type: DecisionType,
        decision_state: DecisionState = DecisionState.DRAFT,
        decision_outcome: DecisionOutcome = DecisionOutcome.UNKNOWN,
        decision_confidence: DecisionConfidence | None = None,
        decision_metadata: DecisionMetadata | None = None,
        decision_inputs: DecisionInputCollection | None = None,
        decision_provenance: DecisionProvenance | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._decision_type = decision_type
        self._decision_state = decision_state
        self._decision_outcome = decision_outcome
        self._decision_confidence = decision_confidence or DecisionConfidence()
        self._decision_metadata = decision_metadata or DecisionMetadata()
        self._decision_inputs = decision_inputs
        self._decision_provenance = decision_provenance
        self.register_validation_hook(validate_decision)

    @property
    def decision_type(self) -> DecisionType:
        return self._decision_type

    @property
    def decision_state(self) -> DecisionState:
        return self._decision_state

    @property
    def decision_outcome(self) -> DecisionOutcome:
        return self._decision_outcome

    @property
    def decision_confidence(self) -> DecisionConfidence:
        return self._decision_confidence

    @property
    def decision_metadata(self) -> DecisionMetadata:
        return self._decision_metadata

    @property
    def decision_inputs(self) -> DecisionInputCollection | None:
        return self._decision_inputs

    @property
    def decision_provenance(self) -> DecisionProvenance | None:
        return self._decision_provenance

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
            "decision_type": self.decision_type.value,
            "decision_state": self.decision_state.value,
            "decision_outcome": self.decision_outcome.value,
            "decision_confidence": self.decision_confidence.to_dict(),
            "decision_metadata": self.decision_metadata.to_dict(),
        }
        if self.decision_inputs is not None:
            payload["decision_inputs"] = self.decision_inputs.to_dict()
        if self.decision_provenance is not None:
            payload["decision_provenance"] = self.decision_provenance.to_dict()
        return payload


def validate_decision(obj: UniversalDecision) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "decision_type", None), DecisionType):
        result.add_error(
            "Decision type must be a DecisionType value.",
            ValidationCategory.SCHEMA,
            field="decision_type",
            code="invalid_decision_type",
        )

    if not isinstance(getattr(obj, "decision_state", None), DecisionState):
        result.add_error(
            "Decision state must be a DecisionState value.",
            ValidationCategory.LIFECYCLE,
            field="decision_state",
            code="invalid_decision_state",
        )

    if not isinstance(getattr(obj, "decision_outcome", None), DecisionOutcome):
        result.add_error(
            "Decision outcome must be a DecisionOutcome value.",
            ValidationCategory.METADATA,
            field="decision_outcome",
            code="invalid_decision_outcome",
        )

    if not isinstance(getattr(obj, "decision_confidence", None), DecisionConfidence):
        result.add_error(
            "Decision confidence must be a DecisionConfidence value.",
            ValidationCategory.METADATA,
            field="decision_confidence",
            code="invalid_decision_confidence",
        )

    if not isinstance(getattr(obj, "decision_metadata", None), DecisionMetadata):
        result.add_error(
            "Decision metadata must be a DecisionMetadata value.",
            ValidationCategory.METADATA,
            field="decision_metadata",
            code="invalid_decision_metadata",
        )

    decision_inputs = getattr(obj, "decision_inputs", None)
    if decision_inputs is not None:
        result.merge(validate_decision_input_collection(decision_inputs))

    decision_provenance = getattr(obj, "decision_provenance", None)
    if decision_provenance is not None:
        result.merge(validate_decision_provenance(decision_provenance))

    return result
