from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class QueryType(StrEnum):
    EXACT_IDENTIFIER = "exact_identifier"
    CATEGORY = "category"
    CLASSIFICATION = "classification"
    PROVENANCE = "provenance"
    EVIDENCE = "evidence"
    METADATA = "metadata"


@dataclass(frozen=True, slots=True)
class QueryMetadata:
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
class QueryConstraint:
    constraint_type: str
    operator: str
    value: Any
    constraint_metadata: QueryMetadata | None = None

    def __post_init__(self) -> None:
        if self.constraint_metadata is None:
            object.__setattr__(self, "constraint_metadata", QueryMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.constraint_metadata or QueryMetadata()
        return {
            "constraint_type": self.constraint_type,
            "operator": self.operator,
            "value": self.value,
            "constraint_metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    query_type: QueryType
    constraints: tuple[QueryConstraint, ...] = ()
    metadata: QueryMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "constraints", tuple(self.constraints))
        if self.metadata is None:
            object.__setattr__(self, "metadata", QueryMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or QueryMetadata()
        return {
            "query_type": self.query_type.value,
            "constraints": [constraint.to_dict() for constraint in self.constraints],
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeQueryContract:
    supported_query_types: tuple[QueryType, ...]
    supported_constraint_types: tuple[str, ...]
    metadata: QueryMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "supported_query_types", tuple(self.supported_query_types))
        object.__setattr__(
            self,
            "supported_constraint_types",
            tuple(self.supported_constraint_types),
        )
        if self.metadata is None:
            object.__setattr__(self, "metadata", QueryMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or QueryMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_query_types": [
                query_type.value for query_type in self.supported_query_types
            ],
            "supported_constraint_types": list(self.supported_constraint_types),
            "metadata": metadata.to_dict(),
        }


def validate_query_metadata(metadata: object, field_prefix: str) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, QueryMetadata):
        result.add_error(
            "Query metadata must be a QueryMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_query_metadata",
        )

    return result


def validate_query_constraint(
    constraint: object,
    field_prefix: str = "constraint",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(constraint, QueryConstraint):
        result.add_error(
            "Query constraint must be a QueryConstraint value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_query_constraint",
        )
        return result

    if not isinstance(constraint.constraint_type, str) or not constraint.constraint_type:
        result.add_error(
            "Query constraint type must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.constraint_type",
            code="invalid_query_constraint_type",
        )

    if not isinstance(constraint.operator, str) or not constraint.operator:
        result.add_error(
            "Query constraint operator must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.operator",
            code="invalid_query_constraint_operator",
        )

    result.merge(
        validate_query_metadata(
            constraint.constraint_metadata,
            f"{field_prefix}.constraint_metadata",
        )
    )

    return result


def validate_knowledge_query(
    query: object,
    field_prefix: str = "query",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(query, KnowledgeQuery):
        result.add_error(
            "Knowledge query must be a KnowledgeQuery value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_knowledge_query",
        )
        return result

    if not isinstance(query.query_type, QueryType):
        result.add_error(
            "Knowledge query type must be a QueryType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.query_type",
            code="invalid_knowledge_query_type",
        )

    if not isinstance(query.constraints, tuple):
        result.add_error(
            "Knowledge query constraints must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.constraints",
            code="invalid_knowledge_query_constraints",
        )
        return result

    for index, constraint in enumerate(query.constraints):
        result.merge(
            validate_query_constraint(
                constraint,
                f"{field_prefix}.constraints[{index}]",
            )
        )

    result.merge(validate_query_metadata(query.metadata, f"{field_prefix}.metadata"))

    return result


def validate_knowledge_query_contract(
    contract: object,
    field_prefix: str = "query_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, KnowledgeQueryContract):
        result.add_error(
            "Knowledge query contract must be a KnowledgeQueryContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_knowledge_query_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Knowledge query contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_knowledge_query_contract_version",
        )

    if not isinstance(contract.supported_query_types, tuple):
        result.add_error(
            "Knowledge query supported query types must be an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_query_types",
            code="invalid_supported_query_types",
        )
    else:
        for index, query_type in enumerate(contract.supported_query_types):
            if not isinstance(query_type, QueryType):
                result.add_error(
                    "Supported query types must be QueryType values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_query_types[{index}]",
                    code="invalid_supported_query_type",
                )

    if not isinstance(contract.supported_constraint_types, tuple):
        result.add_error(
            "Knowledge query supported constraint types must be an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_constraint_types",
            code="invalid_supported_constraint_types",
        )
    else:
        for index, constraint_type in enumerate(contract.supported_constraint_types):
            if not isinstance(constraint_type, str) or not constraint_type:
                result.add_error(
                    "Supported constraint types must be non-empty strings.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_constraint_types[{index}]",
                    code="invalid_supported_constraint_type",
                )

    result.merge(validate_query_metadata(contract.metadata, f"{field_prefix}.metadata"))

    return result
