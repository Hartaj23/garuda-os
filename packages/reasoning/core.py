from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .input import ReasoningInputCollection, validate_reasoning_input_collection
from .provenance import ReasoningProvenance, validate_reasoning_provenance


class ReasoningType(StrEnum):
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    COMPARATIVE = "comparative"
    CAUSAL = "causal"
    TEMPORAL = "temporal"
    DEPENDENCY = "dependency"
    CONSISTENCY = "consistency"


class ReasoningState(StrEnum):
    DRAFT = "draft"
    EVALUATED = "evaluated"
    VALIDATED = "validated"
    ACCEPTED = "accepted"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class ReasoningConfidence:
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
class ReasoningMetadata:
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


class UniversalReasoning(CanonicalObject):
    """Platform-level reasoning object."""

    def __init__(
        self,
        reasoning_type: ReasoningType,
        reasoning_state: ReasoningState = ReasoningState.DRAFT,
        reasoning_confidence: ReasoningConfidence | None = None,
        reasoning_metadata: ReasoningMetadata | None = None,
        reasoning_inputs: ReasoningInputCollection | None = None,
        reasoning_provenance: ReasoningProvenance | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._reasoning_type = reasoning_type
        self._reasoning_state = reasoning_state
        self._reasoning_confidence = reasoning_confidence or ReasoningConfidence()
        self._reasoning_metadata = reasoning_metadata or ReasoningMetadata()
        self._reasoning_inputs = reasoning_inputs
        self._reasoning_provenance = reasoning_provenance
        self.register_validation_hook(validate_reasoning)

    @property
    def reasoning_type(self) -> ReasoningType:
        return self._reasoning_type

    @property
    def reasoning_state(self) -> ReasoningState:
        return self._reasoning_state

    @property
    def reasoning_confidence(self) -> ReasoningConfidence:
        return self._reasoning_confidence

    @property
    def reasoning_metadata(self) -> ReasoningMetadata:
        return self._reasoning_metadata

    @property
    def reasoning_inputs(self) -> ReasoningInputCollection | None:
        return self._reasoning_inputs

    @property
    def reasoning_provenance(self) -> ReasoningProvenance | None:
        return self._reasoning_provenance

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
            "reasoning_type": self.reasoning_type.value,
            "reasoning_state": self.reasoning_state.value,
            "reasoning_confidence": self.reasoning_confidence.to_dict(),
            "reasoning_metadata": self.reasoning_metadata.to_dict(),
        }
        if self.reasoning_inputs is not None:
            payload["reasoning_inputs"] = self.reasoning_inputs.to_dict()
        if self.reasoning_provenance is not None:
            payload["reasoning_provenance"] = self.reasoning_provenance.to_dict()
        return payload


def validate_reasoning(obj: UniversalReasoning) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "reasoning_type", None), ReasoningType):
        result.add_error(
            "Reasoning type must be a ReasoningType value.",
            ValidationCategory.SCHEMA,
            field="reasoning_type",
            code="invalid_reasoning_type",
        )

    if not isinstance(getattr(obj, "reasoning_state", None), ReasoningState):
        result.add_error(
            "Reasoning state must be a ReasoningState value.",
            ValidationCategory.LIFECYCLE,
            field="reasoning_state",
            code="invalid_reasoning_state",
        )

    if not isinstance(getattr(obj, "reasoning_confidence", None), ReasoningConfidence):
        result.add_error(
            "Reasoning confidence must be a ReasoningConfidence value.",
            ValidationCategory.METADATA,
            field="reasoning_confidence",
            code="invalid_reasoning_confidence",
        )

    if not isinstance(getattr(obj, "reasoning_metadata", None), ReasoningMetadata):
        result.add_error(
            "Reasoning metadata must be a ReasoningMetadata value.",
            ValidationCategory.METADATA,
            field="reasoning_metadata",
            code="invalid_reasoning_metadata",
        )

    reasoning_inputs = getattr(obj, "reasoning_inputs", None)
    if reasoning_inputs is not None:
        result.merge(validate_reasoning_input_collection(reasoning_inputs))

    reasoning_provenance = getattr(obj, "reasoning_provenance", None)
    if reasoning_provenance is not None:
        result.merge(validate_reasoning_provenance(reasoning_provenance))

    return result
