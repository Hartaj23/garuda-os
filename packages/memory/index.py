from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.objects import ValidationCategory, ValidationResult


class IndexFieldType(StrEnum):
    STRING = "string"
    UUID = "uuid"
    DATETIME = "datetime"
    ENUM = "enum"
    INTEGER = "integer"
    BOOLEAN = "boolean"


@dataclass(frozen=True, slots=True)
class IndexField:
    field_name: str
    field_type: IndexFieldType
    indexable: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "field_name": self.field_name,
            "field_type": self.field_type.value,
            "indexable": self.indexable,
        }


@dataclass(frozen=True, slots=True)
class IndexMetadata:
    schema_version: str = "1.0"
    descriptor_version: int = 1
    platform_compatibility: str = "garuda-memory-v1"

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "descriptor_version": self.descriptor_version,
            "platform_compatibility": self.platform_compatibility,
        }


@dataclass(frozen=True, slots=True)
class MemoryIndexDescriptor:
    memory_id: str
    memory_type: str
    origin: str
    acquisition_method: str
    acquisition_channel: str
    lifecycle_state: str
    confidence: str
    created_at: str

    def to_dict(self) -> dict[str, str]:
        return {
            "memory_id": self.memory_id,
            "memory_type": self.memory_type,
            "origin": self.origin,
            "acquisition_method": self.acquisition_method,
            "acquisition_channel": self.acquisition_channel,
            "lifecycle_state": self.lifecycle_state,
            "confidence": self.confidence,
            "created_at": self.created_at,
        }


@dataclass(frozen=True, slots=True)
class IndexContract:
    metadata: IndexMetadata
    fields: tuple[IndexField, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "fields", tuple(self.fields))

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "fields": [field.to_dict() for field in self.fields],
        }


DEFAULT_MEMORY_INDEX_FIELDS: tuple[IndexField, ...] = (
    IndexField("memory_id", IndexFieldType.UUID),
    IndexField("memory_type", IndexFieldType.ENUM),
    IndexField("origin", IndexFieldType.ENUM),
    IndexField("acquisition_method", IndexFieldType.ENUM),
    IndexField("acquisition_channel", IndexFieldType.ENUM),
    IndexField("lifecycle_state", IndexFieldType.ENUM),
    IndexField("confidence", IndexFieldType.ENUM),
    IndexField("created_at", IndexFieldType.DATETIME),
)


def validate_index_field(field: IndexField) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(field.field_name, str) or not field.field_name:
        result.add_error(
            "Index field name must be a non-empty string.",
            ValidationCategory.METADATA,
            field="field_name",
            code="invalid_index_field_name",
        )

    if not isinstance(field.field_type, IndexFieldType):
        result.add_error(
            "Index field type must be an IndexFieldType value.",
            ValidationCategory.METADATA,
            field="field_type",
            code="invalid_index_field_type",
        )

    if not isinstance(field.indexable, bool):
        result.add_error(
            "Index field indexability must be a boolean.",
            ValidationCategory.METADATA,
            field="indexable",
            code="invalid_indexability",
        )

    return result


def validate_index_metadata(metadata: IndexMetadata) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata.schema_version, str) or not metadata.schema_version:
        result.add_error(
            "Index metadata schema version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field="schema_version",
            code="invalid_index_schema_version",
        )

    if not isinstance(metadata.descriptor_version, int) or metadata.descriptor_version < 1:
        result.add_error(
            "Index descriptor version must be a positive integer.",
            ValidationCategory.VERSION,
            field="descriptor_version",
            code="invalid_index_descriptor_version",
        )

    if (
        not isinstance(metadata.platform_compatibility, str)
        or not metadata.platform_compatibility
    ):
        result.add_error(
            "Index platform compatibility must be a non-empty string.",
            ValidationCategory.METADATA,
            field="platform_compatibility",
            code="invalid_index_platform_compatibility",
        )

    return result


def validate_index_contract(contract: IndexContract) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract.metadata, IndexMetadata):
        result.add_error(
            "Index contract metadata must be an IndexMetadata value.",
            ValidationCategory.METADATA,
            field="metadata",
            code="invalid_index_contract_metadata",
        )
    else:
        result.merge(validate_index_metadata(contract.metadata))

    if not isinstance(contract.fields, tuple):
        result.add_error(
            "Index contract fields must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="fields",
            code="invalid_index_contract_fields",
        )
        return result

    seen_fields: set[str] = set()
    for index, field in enumerate(contract.fields):
        if not isinstance(field, IndexField):
            result.add_error(
                "Index contract fields must be IndexField values.",
                ValidationCategory.METADATA,
                field=f"fields[{index}]",
                code="invalid_index_contract_field",
            )
            continue

        result.merge(validate_index_field(field))
        if field.field_name in seen_fields:
            result.add_error(
                "Index contract field names must be unique.",
                ValidationCategory.METADATA,
                field=f"fields[{index}].field_name",
                code="duplicate_index_field_name",
            )
        seen_fields.add(field.field_name)

    return result
