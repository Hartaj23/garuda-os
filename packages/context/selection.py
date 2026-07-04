from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class SelectionType(StrEnum):
    EXACT_IDENTIFIER = "exact_identifier"
    SOURCE_BASED = "source_based"
    SCOPE_BASED = "scope_based"
    TYPE_BASED = "type_based"
    COMPOSITION_BASED = "composition_based"


@dataclass(frozen=True, slots=True)
class SelectionMetadata:
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
class SelectionCriterion:
    criterion_name: str
    operator: str
    criterion_value: Any

    def to_dict(self) -> dict[str, object]:
        return {
            "criterion_name": self.criterion_name,
            "operator": self.operator,
            "criterion_value": self.criterion_value,
        }


@dataclass(frozen=True, slots=True)
class ContextSelectionRequest:
    selection_type: SelectionType
    criteria: tuple[SelectionCriterion, ...] = ()
    metadata: SelectionMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "criteria", tuple(self.criteria))
        if self.metadata is None:
            object.__setattr__(self, "metadata", SelectionMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or SelectionMetadata()
        return {
            "selection_type": self.selection_type.value,
            "criteria": [criterion.to_dict() for criterion in self.criteria],
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ContextSelectionContract:
    supported_selection_types: tuple[SelectionType, ...]
    supported_criteria: tuple[str, ...]
    metadata: SelectionMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supported_selection_types",
            tuple(self.supported_selection_types),
        )
        object.__setattr__(self, "supported_criteria", tuple(self.supported_criteria))
        if self.metadata is None:
            object.__setattr__(self, "metadata", SelectionMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or SelectionMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_selection_types": [
                selection_type.value for selection_type in self.supported_selection_types
            ],
            "supported_criteria": list(self.supported_criteria),
            "metadata": metadata.to_dict(),
        }


def validate_selection_metadata(
    metadata: object,
    field_prefix: str = "selection_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, SelectionMetadata):
        result.add_error(
            "Selection metadata must be a SelectionMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_selection_metadata",
        )

    return result


def validate_selection_criterion(
    criterion: object,
    field_prefix: str = "criterion",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(criterion, SelectionCriterion):
        result.add_error(
            "Selection criterion must be a SelectionCriterion value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_selection_criterion",
        )
        return result

    if not isinstance(criterion.criterion_name, str) or not criterion.criterion_name:
        result.add_error(
            "Selection criterion name must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.criterion_name",
            code="invalid_selection_criterion_name",
        )

    if not isinstance(criterion.operator, str) or not criterion.operator:
        result.add_error(
            "Selection criterion operator must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.operator",
            code="invalid_selection_criterion_operator",
        )

    return result


def validate_context_selection_request(
    request: object,
    field_prefix: str = "selection_request",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(request, ContextSelectionRequest):
        result.add_error(
            "Context selection request must be a ContextSelectionRequest value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_selection_request",
        )
        return result

    if not isinstance(request.selection_type, SelectionType):
        result.add_error(
            "Context selection type must be a SelectionType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.selection_type",
            code="invalid_selection_type",
        )

    if not isinstance(request.criteria, tuple):
        result.add_error(
            "Context selection criteria must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.criteria",
            code="invalid_selection_criteria",
        )
    else:
        for index, criterion in enumerate(request.criteria):
            result.merge(
                validate_selection_criterion(
                    criterion,
                    f"{field_prefix}.criteria[{index}]",
                )
            )

    result.merge(validate_selection_metadata(request.metadata, f"{field_prefix}.metadata"))

    return result


def validate_context_selection_contract(
    contract: object,
    field_prefix: str = "selection_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, ContextSelectionContract):
        result.add_error(
            "Context selection contract must be a ContextSelectionContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_selection_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Context selection contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_context_selection_contract_version",
        )

    if not isinstance(contract.supported_selection_types, tuple):
        result.add_error(
            "Supported selection types must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_selection_types",
            code="invalid_supported_selection_types",
        )
    else:
        for index, selection_type in enumerate(contract.supported_selection_types):
            if not isinstance(selection_type, SelectionType):
                result.add_error(
                    "Supported selection types must be SelectionType values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_selection_types[{index}]",
                    code="invalid_supported_selection_type",
                )

    if not isinstance(contract.supported_criteria, tuple):
        result.add_error(
            "Supported criteria must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_criteria",
            code="invalid_supported_criteria",
        )
    else:
        for index, criterion_name in enumerate(contract.supported_criteria):
            if not isinstance(criterion_name, str) or not criterion_name:
                result.add_error(
                    "Supported criteria must be non-empty strings.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_criteria[{index}]",
                    code="invalid_supported_criterion",
                )

    result.merge(validate_selection_metadata(contract.metadata, f"{field_prefix}.metadata"))

    return result
