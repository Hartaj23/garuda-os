from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


@dataclass(frozen=True, slots=True)
class RuntimeValidationMetadata:
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


def validate_runtime_validation_metadata(
    metadata: object,
    field_prefix: str = "validation_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, RuntimeValidationMetadata):
        result.add_error(
            "Validation metadata must be a RuntimeValidationMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_validation_metadata",
        )
        return result

    if not isinstance(metadata.values, tuple):
        result.add_error(
            "Validation metadata values must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.values",
            code="invalid_validation_metadata_values",
        )

    return result
