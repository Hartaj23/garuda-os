from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from packages.objects import LifecycleState, ValidationCategory, ValidationResult

from .core import MemoryConfidence, MemoryType
from .source import AcquisitionChannel, AcquisitionMethod, MemoryOrigin


class RetrievalStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    EMPTY = "empty"
    UNSUPPORTED = "unsupported"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class RetrievalMetadata:
    contract_version: str = "1.0"
    request_timestamp: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    response_timestamp: datetime | None = None
    platform_compatibility: str = "garuda-memory-v1"

    def to_dict(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "request_timestamp": self.request_timestamp.isoformat(),
            "response_timestamp": self.response_timestamp.isoformat()
            if self.response_timestamp
            else None,
            "platform_compatibility": self.platform_compatibility,
        }


@dataclass(frozen=True, slots=True)
class MemoryRetrievalCriteria:
    memory_types: tuple[MemoryType, ...] = ()
    origins: tuple[MemoryOrigin, ...] = ()
    acquisition_methods: tuple[AcquisitionMethod, ...] = ()
    acquisition_channels: tuple[AcquisitionChannel, ...] = ()
    confidence: MemoryConfidence | None = None
    lifecycle_states: tuple[LifecycleState, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "memory_types", tuple(self.memory_types))
        object.__setattr__(self, "origins", tuple(self.origins))
        object.__setattr__(self, "acquisition_methods", tuple(self.acquisition_methods))
        object.__setattr__(self, "acquisition_channels", tuple(self.acquisition_channels))
        object.__setattr__(self, "lifecycle_states", tuple(self.lifecycle_states))

    def to_dict(self) -> dict[str, object]:
        return {
            "memory_types": [memory_type.value for memory_type in self.memory_types],
            "origins": [origin.value for origin in self.origins],
            "acquisition_methods": [method.value for method in self.acquisition_methods],
            "acquisition_channels": [channel.value for channel in self.acquisition_channels],
            "confidence": self.confidence.value if self.confidence else None,
            "lifecycle_states": [state.value for state in self.lifecycle_states],
        }


@dataclass(frozen=True, slots=True)
class MemoryRetrievalRequest:
    request_id: str
    criteria: MemoryRetrievalCriteria
    metadata: RetrievalMetadata = field(default_factory=RetrievalMetadata)
    schema_version: str = "1.0"

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "schema_version": self.schema_version,
            "criteria": self.criteria.to_dict(),
            "metadata": self.metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class MemoryRetrievalResponse:
    request_id: str
    metadata: RetrievalMetadata
    status: RetrievalStatus = RetrievalStatus.PENDING
    memory_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "memory_ids", tuple(self.memory_ids))

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "memory_ids": list(self.memory_ids),
        }


def validate_retrieval_metadata(metadata: RetrievalMetadata) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata.contract_version, str) or not metadata.contract_version:
        result.add_error(
            "Retrieval contract version must be a non-empty string.",
            ValidationCategory.VERSION,
            field="contract_version",
            code="invalid_retrieval_contract_version",
        )

    if not hasattr(metadata.request_timestamp, "isoformat"):
        result.add_error(
            "Retrieval request timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="request_timestamp",
            code="invalid_retrieval_request_timestamp",
        )

    if metadata.response_timestamp is not None and not hasattr(
        metadata.response_timestamp,
        "isoformat",
    ):
        result.add_error(
            "Retrieval response timestamp must be datetime-like when provided.",
            ValidationCategory.METADATA,
            field="response_timestamp",
            code="invalid_retrieval_response_timestamp",
        )

    if (
        not isinstance(metadata.platform_compatibility, str)
        or not metadata.platform_compatibility
    ):
        result.add_error(
            "Retrieval platform compatibility must be a non-empty string.",
            ValidationCategory.METADATA,
            field="platform_compatibility",
            code="invalid_retrieval_platform_compatibility",
        )

    return result


def validate_retrieval_criteria(criteria: MemoryRetrievalCriteria) -> ValidationResult:
    result = ValidationResult()

    _validate_tuple_values(result, criteria.memory_types, MemoryType, "memory_types")
    _validate_tuple_values(result, criteria.origins, MemoryOrigin, "origins")
    _validate_tuple_values(
        result,
        criteria.acquisition_methods,
        AcquisitionMethod,
        "acquisition_methods",
    )
    _validate_tuple_values(
        result,
        criteria.acquisition_channels,
        AcquisitionChannel,
        "acquisition_channels",
    )
    _validate_tuple_values(result, criteria.lifecycle_states, LifecycleState, "lifecycle_states")

    if criteria.confidence is not None and not isinstance(criteria.confidence, MemoryConfidence):
        result.add_error(
            "Retrieval confidence must be a MemoryConfidence value when provided.",
            ValidationCategory.METADATA,
            field="confidence",
            code="invalid_retrieval_confidence",
        )

    return result


def validate_retrieval_request(request: MemoryRetrievalRequest) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(request.request_id, str) or not request.request_id:
        result.add_error(
            "Retrieval request identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="request_id",
            code="invalid_retrieval_request_id",
        )

    if not isinstance(request.schema_version, str) or not request.schema_version:
        result.add_error(
            "Retrieval request schema version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field="schema_version",
            code="invalid_retrieval_schema_version",
        )

    if not isinstance(request.criteria, MemoryRetrievalCriteria):
        result.add_error(
            "Retrieval request criteria must be a MemoryRetrievalCriteria value.",
            ValidationCategory.METADATA,
            field="criteria",
            code="invalid_retrieval_criteria",
        )
    else:
        result.merge(validate_retrieval_criteria(request.criteria))

    if not isinstance(request.metadata, RetrievalMetadata):
        result.add_error(
            "Retrieval request metadata must be a RetrievalMetadata value.",
            ValidationCategory.METADATA,
            field="metadata",
            code="invalid_retrieval_request_metadata",
        )
    else:
        result.merge(validate_retrieval_metadata(request.metadata))

    return result


def validate_retrieval_response(response: MemoryRetrievalResponse) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(response.request_id, str) or not response.request_id:
        result.add_error(
            "Retrieval response request identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="request_id",
            code="invalid_retrieval_response_request_id",
        )

    if not isinstance(response.metadata, RetrievalMetadata):
        result.add_error(
            "Retrieval response metadata must be a RetrievalMetadata value.",
            ValidationCategory.METADATA,
            field="metadata",
            code="invalid_retrieval_response_metadata",
        )
    else:
        result.merge(validate_retrieval_metadata(response.metadata))

    if not isinstance(response.status, RetrievalStatus):
        result.add_error(
            "Retrieval response status must be a RetrievalStatus value.",
            ValidationCategory.METADATA,
            field="status",
            code="invalid_retrieval_status",
        )

    if not isinstance(response.memory_ids, tuple):
        result.add_error(
            "Retrieval response memory identifiers must be an immutable tuple.",
            ValidationCategory.METADATA,
            field="memory_ids",
            code="invalid_retrieval_memory_ids",
        )
    else:
        for index, memory_id in enumerate(response.memory_ids):
            if not isinstance(memory_id, str) or not memory_id:
                result.add_error(
                    "Retrieval response memory identifiers must be non-empty strings.",
                    ValidationCategory.IDENTITY,
                    field=f"memory_ids[{index}]",
                    code="invalid_retrieval_memory_id",
                )

    return result


def _validate_tuple_values(
    result: ValidationResult,
    values: tuple[object, ...],
    expected_type: type[object],
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        result.add_error(
            "Retrieval criteria values must be stored as immutable tuples.",
            ValidationCategory.METADATA,
            field=field_name,
            code="invalid_retrieval_criteria_collection",
        )
        return

    for index, value in enumerate(values):
        if not isinstance(value, expected_type):
            result.add_error(
                "Retrieval criteria values must use the expected enum type.",
                ValidationCategory.METADATA,
                field=f"{field_name}[{index}]",
                code="invalid_retrieval_criteria_value",
            )
