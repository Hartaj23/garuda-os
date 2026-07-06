from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult


class InterfaceFoundationCategory(StrEnum):
    CORE = "core"


@dataclass(frozen=True, slots=True)
class InterfaceFoundationMetadata:
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


class InterfaceFoundation(CanonicalObject):
    """Platform-level interface foundation object for GAR-SPRINT-0010 Mission Alpha."""

    def __init__(
        self,
        foundation_category: InterfaceFoundationCategory = InterfaceFoundationCategory.CORE,
        foundation_metadata: InterfaceFoundationMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._foundation_category = foundation_category
        self._foundation_metadata = foundation_metadata or InterfaceFoundationMetadata()
        self.register_validation_hook(validate_interface_foundation)

    @property
    def foundation_category(self) -> InterfaceFoundationCategory:
        return self._foundation_category

    @property
    def foundation_metadata(self) -> InterfaceFoundationMetadata:
        return self._foundation_metadata

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
            "foundation_category": self.foundation_category.value,
            "foundation_metadata": self.foundation_metadata.to_dict(),
        }


def validate_interface_foundation(obj: InterfaceFoundation) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "foundation_category", None), InterfaceFoundationCategory):
        result.add_error(
            "Foundation category must be an InterfaceFoundationCategory value.",
            ValidationCategory.SCHEMA,
            field="foundation_category",
            code="invalid_foundation_category",
        )

    if not isinstance(getattr(obj, "foundation_metadata", None), InterfaceFoundationMetadata):
        result.add_error(
            "Foundation metadata must be an InterfaceFoundationMetadata value.",
            ValidationCategory.METADATA,
            field="foundation_metadata",
            code="invalid_foundation_metadata",
        )

    return result
