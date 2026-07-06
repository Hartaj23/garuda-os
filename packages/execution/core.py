from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .input import ExecutionInputCollection, validate_execution_input_collection
from .provenance import ExecutionProvenance, validate_execution_provenance


class ExecutionType(StrEnum):
    ACTION = "action"
    WORKFLOW = "workflow"
    PROCEDURE = "procedure"
    COMMAND = "command"
    REVIEW = "review"
    OBSERVATION = "observation"


class ExecutionState(StrEnum):
    DRAFT = "draft"
    PLANNED = "planned"
    READY = "ready"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ExecutionOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ExecutionConfidence:
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
class ExecutionMetadata:
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


class UniversalExecution(CanonicalObject):
    """Platform-level execution object."""

    def __init__(
        self,
        execution_type: ExecutionType,
        execution_state: ExecutionState = ExecutionState.DRAFT,
        execution_outcome: ExecutionOutcome = ExecutionOutcome.UNKNOWN,
        execution_confidence: ExecutionConfidence | None = None,
        execution_metadata: ExecutionMetadata | None = None,
        execution_inputs: ExecutionInputCollection | None = None,
        execution_provenance: ExecutionProvenance | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._execution_type = execution_type
        self._execution_state = execution_state
        self._execution_outcome = execution_outcome
        self._execution_confidence = execution_confidence or ExecutionConfidence()
        self._execution_metadata = execution_metadata or ExecutionMetadata()
        self._execution_inputs = execution_inputs
        self._execution_provenance = execution_provenance
        self.register_validation_hook(validate_execution)

    @property
    def execution_type(self) -> ExecutionType:
        return self._execution_type

    @property
    def execution_state(self) -> ExecutionState:
        return self._execution_state

    @property
    def execution_outcome(self) -> ExecutionOutcome:
        return self._execution_outcome

    @property
    def execution_confidence(self) -> ExecutionConfidence:
        return self._execution_confidence

    @property
    def execution_metadata(self) -> ExecutionMetadata:
        return self._execution_metadata

    @property
    def execution_inputs(self) -> ExecutionInputCollection | None:
        return self._execution_inputs

    @property
    def execution_provenance(self) -> ExecutionProvenance | None:
        return self._execution_provenance

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
            "execution_type": self.execution_type.value,
            "execution_state": self.execution_state.value,
            "execution_outcome": self.execution_outcome.value,
            "execution_confidence": self.execution_confidence.to_dict(),
            "execution_metadata": self.execution_metadata.to_dict(),
        }
        if self.execution_inputs is not None:
            payload["execution_inputs"] = self.execution_inputs.to_dict()
        if self.execution_provenance is not None:
            payload["execution_provenance"] = self.execution_provenance.to_dict()
        return payload


def validate_execution(obj: UniversalExecution) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "execution_type", None), ExecutionType):
        result.add_error(
            "Execution type must be an ExecutionType value.",
            ValidationCategory.SCHEMA,
            field="execution_type",
            code="invalid_execution_type",
        )

    if not isinstance(getattr(obj, "execution_state", None), ExecutionState):
        result.add_error(
            "Execution state must be an ExecutionState value.",
            ValidationCategory.LIFECYCLE,
            field="execution_state",
            code="invalid_execution_state",
        )

    if not isinstance(getattr(obj, "execution_outcome", None), ExecutionOutcome):
        result.add_error(
            "Execution outcome must be an ExecutionOutcome value.",
            ValidationCategory.METADATA,
            field="execution_outcome",
            code="invalid_execution_outcome",
        )

    if not isinstance(getattr(obj, "execution_confidence", None), ExecutionConfidence):
        result.add_error(
            "Execution confidence must be an ExecutionConfidence value.",
            ValidationCategory.METADATA,
            field="execution_confidence",
            code="invalid_execution_confidence",
        )

    if not isinstance(getattr(obj, "execution_metadata", None), ExecutionMetadata):
        result.add_error(
            "Execution metadata must be an ExecutionMetadata value.",
            ValidationCategory.METADATA,
            field="execution_metadata",
            code="invalid_execution_metadata",
        )

    execution_inputs = getattr(obj, "execution_inputs", None)
    if execution_inputs is not None:
        result.merge(validate_execution_input_collection(execution_inputs))

    execution_provenance = getattr(obj, "execution_provenance", None)
    if execution_provenance is not None:
        result.merge(validate_execution_provenance(execution_provenance))

    return result
