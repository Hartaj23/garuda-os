from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class KnowledgeCategory(StrEnum):
    FACTUAL = "factual"
    CONCEPTUAL = "conceptual"
    PROCEDURAL = "procedural"
    STRUCTURAL = "structural"
    OBSERVATIONAL = "observational"


@dataclass(frozen=True, slots=True)
class ClassificationMetadata:
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


@dataclass(frozen=True, slots=True)
class ClassificationDimension:
    dimension_name: str
    dimension_value: str | None = None
    dimension_metadata: ClassificationMetadata | None = None

    def __post_init__(self) -> None:
        if self.dimension_metadata is None:
            object.__setattr__(self, "dimension_metadata", ClassificationMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.dimension_metadata or ClassificationMetadata()
        return {
            "dimension_name": self.dimension_name,
            "dimension_value": self.dimension_value,
            "dimension_metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ClassificationDescriptor:
    category: KnowledgeCategory
    dimensions: tuple[ClassificationDimension, ...] = ()
    classification_metadata: ClassificationMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "dimensions", tuple(self.dimensions))
        if self.classification_metadata is None:
            object.__setattr__(self, "classification_metadata", ClassificationMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.classification_metadata or ClassificationMetadata()
        return {
            "category": self.category.value,
            "dimensions": [dimension.to_dict() for dimension in self.dimensions],
            "classification_metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeClassificationContract:
    supported_categories: tuple[KnowledgeCategory, ...]
    supported_dimensions: tuple[ClassificationDimension, ...]
    metadata: ClassificationMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "supported_categories", tuple(self.supported_categories))
        object.__setattr__(self, "supported_dimensions", tuple(self.supported_dimensions))
        if self.metadata is None:
            object.__setattr__(self, "metadata", ClassificationMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ClassificationMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_categories": [
                category.value for category in self.supported_categories
            ],
            "supported_dimensions": [
                dimension.to_dict() for dimension in self.supported_dimensions
            ],
            "metadata": metadata.to_dict(),
        }


def validate_classification_metadata(metadata: object, field_prefix: str) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, ClassificationMetadata):
        result.add_error(
            "Classification metadata must be a ClassificationMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_metadata",
        )

    return result


def validate_classification_dimension(
    dimension: object,
    field_prefix: str = "dimension",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(dimension, ClassificationDimension):
        result.add_error(
            "Classification dimension must be a ClassificationDimension value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_dimension",
        )
        return result

    if not isinstance(dimension.dimension_name, str) or not dimension.dimension_name:
        result.add_error(
            "Classification dimension name must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.dimension_name",
            code="invalid_classification_dimension_name",
        )

    if dimension.dimension_value is not None and not isinstance(
        dimension.dimension_value,
        str,
    ):
        result.add_error(
            "Classification dimension value must be a string when present.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.dimension_value",
            code="invalid_classification_dimension_value",
        )

    result.merge(
        validate_classification_metadata(
            dimension.dimension_metadata,
            f"{field_prefix}.dimension_metadata",
        )
    )

    return result


def validate_classification_descriptor(
    descriptor: object,
    field_prefix: str = "descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, ClassificationDescriptor):
        result.add_error(
            "Classification descriptor must be a ClassificationDescriptor value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_descriptor",
        )
        return result

    if not isinstance(descriptor.category, KnowledgeCategory):
        result.add_error(
            "Classification descriptor category must be a KnowledgeCategory value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.category",
            code="invalid_classification_category",
        )

    if not isinstance(descriptor.dimensions, tuple):
        result.add_error(
            "Classification descriptor dimensions must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.dimensions",
            code="invalid_classification_descriptor_dimensions",
        )
        return result

    for index, dimension in enumerate(descriptor.dimensions):
        result.merge(
            validate_classification_dimension(
                dimension,
                f"{field_prefix}.dimensions[{index}]",
            )
        )

    result.merge(
        validate_classification_metadata(
            descriptor.classification_metadata,
            f"{field_prefix}.classification_metadata",
        )
    )

    return result


def validate_knowledge_classification_contract(
    contract: object,
    field_prefix: str = "classification_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, KnowledgeClassificationContract):
        result.add_error(
            "Knowledge classification contract must be a KnowledgeClassificationContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_knowledge_classification_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Knowledge classification contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_knowledge_classification_contract_version",
        )

    if not isinstance(contract.supported_categories, tuple):
        result.add_error(
            "Knowledge classification supported categories must be an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_categories",
            code="invalid_supported_knowledge_categories",
        )
    else:
        for index, category in enumerate(contract.supported_categories):
            if not isinstance(category, KnowledgeCategory):
                result.add_error(
                    "Supported classification categories must be KnowledgeCategory values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_categories[{index}]",
                    code="invalid_supported_knowledge_category",
                )

    if not isinstance(contract.supported_dimensions, tuple):
        result.add_error(
            "Knowledge classification supported dimensions must be an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_dimensions",
            code="invalid_supported_classification_dimensions",
        )
    else:
        for index, dimension in enumerate(contract.supported_dimensions):
            result.merge(
                validate_classification_dimension(
                    dimension,
                    f"{field_prefix}.supported_dimensions[{index}]",
                )
            )

    result.merge(
        validate_classification_metadata(
            contract.metadata,
            f"{field_prefix}.metadata",
        )
    )

    return result
