from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import StrEnum
from typing import Any
from uuid import UUID


class ValidationSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationCategory(StrEnum):
    IDENTITY = "identity"
    METADATA = "metadata"
    LIFECYCLE = "lifecycle"
    BEHAVIOR = "behavior"
    RELATIONSHIPS = "relationships"
    SCHEMA = "schema"
    VERSION = "version"


@dataclass(slots=True)
class ValidationError:
    message: str
    category: ValidationCategory
    severity: ValidationSeverity = ValidationSeverity.ERROR
    field: str | None = None
    code: str | None = None
    context: dict[str, Any] = dataclass_field(default_factory=dict)


@dataclass(slots=True)
class ValidationResult:
    errors: list[ValidationError] = dataclass_field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not any(
            error.severity in {ValidationSeverity.ERROR, ValidationSeverity.CRITICAL}
            for error in self.errors
        )

    def add_error(
        self,
        message: str,
        category: ValidationCategory,
        severity: ValidationSeverity = ValidationSeverity.ERROR,
        field: str | None = None,
        code: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> ValidationError:
        error = ValidationError(
            message=message,
            category=category,
            severity=severity,
            field=field,
            code=code,
            context=context or {},
        )
        self.errors.append(error)
        return error

    def add_warning(
        self,
        message: str,
        category: ValidationCategory,
        field: str | None = None,
        code: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> ValidationError:
        return self.add_error(
            message=message,
            category=category,
            severity=ValidationSeverity.WARNING,
            field=field,
            code=code,
            context=context,
        )

    def merge(self, other: ValidationResult | ValidationError | None) -> ValidationResult:
        if other is None:
            return self
        if isinstance(other, ValidationError):
            self.errors.append(other)
            return self
        self.errors.extend(other.errors)
        return self


def validate_object_identity(obj: Any) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(getattr(obj, "object_id", None), UUID):
        result.add_error(
            "Object identity must be a UUID.",
            ValidationCategory.IDENTITY,
            field="object_id",
            code="invalid_object_id",
        )
    if not isinstance(getattr(obj, "object_type", None), str) or not obj.object_type:
        result.add_error(
            "Object type must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="object_type",
            code="invalid_object_type",
        )
    return result


def validate_object_metadata(obj: Any) -> ValidationResult:
    result = ValidationResult()
    metadata = getattr(obj, "metadata", None)
    if not isinstance(getattr(metadata, "values", None), dict):
        result.add_error(
            "Object metadata must expose a values dictionary.",
            ValidationCategory.METADATA,
            field="metadata",
            code="invalid_metadata",
        )
    if not isinstance(getattr(obj, "tags", None), tuple):
        result.add_error(
            "Object tags must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="tags",
            code="invalid_tags",
        )
    return result


def validate_object_lifecycle(obj: Any) -> ValidationResult:
    result = ValidationResult()
    lifecycle_state = getattr(obj, "lifecycle_state", None)
    if not hasattr(lifecycle_state, "value"):
        result.add_error(
            "Object lifecycle state must be an enum value.",
            ValidationCategory.LIFECYCLE,
            field="lifecycle_state",
            code="invalid_lifecycle_state",
        )
    return result


def validate_object_behavior(obj: Any) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(getattr(obj, "behaviors", None), dict):
        result.add_error(
            "Object behaviors must be stored as a dictionary.",
            ValidationCategory.BEHAVIOR,
            field="behaviors",
            code="invalid_behaviors",
        )
    return result


def validate_object_relationships(obj: Any) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(getattr(obj, "relationships", None), dict):
        result.add_error(
            "Object relationships must be stored as a dictionary.",
            ValidationCategory.RELATIONSHIPS,
            field="relationships",
            code="invalid_relationships",
        )
    return result


def validate_object_schema(obj: Any) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(getattr(obj, "schema_version", None), str) or not obj.schema_version:
        result.add_error(
            "Object schema version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field="schema_version",
            code="invalid_schema_version",
        )
    return result


def validate_object_version(obj: Any) -> ValidationResult:
    result = ValidationResult()
    object_version = getattr(obj, "object_version", None)
    if not isinstance(object_version, int) or object_version < 1:
        result.add_error(
            "Object version must be a positive integer.",
            ValidationCategory.VERSION,
            field="object_version",
            code="invalid_object_version",
        )
    return result


def validate_object(obj: Any) -> ValidationResult:
    result = ValidationResult()
    result.merge(validate_object_identity(obj))
    result.merge(validate_object_metadata(obj))
    result.merge(validate_object_lifecycle(obj))
    result.merge(validate_object_behavior(obj))
    result.merge(validate_object_relationships(obj))
    result.merge(validate_object_schema(obj))
    result.merge(validate_object_version(obj))
    return result
