from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class RuntimeLifecycleState(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class RuntimeLifecycleMetadata:
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


def validate_runtime_lifecycle_metadata(
    metadata: object,
    field_prefix: str = "lifecycle_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, RuntimeLifecycleMetadata):
        result.add_error(
            "Lifecycle metadata must be a RuntimeLifecycleMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_lifecycle_metadata",
        )
        return result

    if not isinstance(metadata.values, tuple):
        result.add_error(
            "Lifecycle metadata values must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.values",
            code="invalid_lifecycle_metadata_values",
        )

    return result


def validate_runtime_lifecycle_state(
    lifecycle_state: object,
    field_prefix: str = "lifecycle_state",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(lifecycle_state, RuntimeLifecycleState):
        result.add_error(
            "Lifecycle state must be a RuntimeLifecycleState value.",
            ValidationCategory.LIFECYCLE,
            field=field_prefix,
            code="invalid_lifecycle_state",
        )

    return result
