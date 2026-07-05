from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class StrategyType(StrEnum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    COMPARATIVE = "comparative"
    ELIMINATION = "elimination"
    DEPENDENCY = "dependency"
    VALIDATION = "validation"


@dataclass(frozen=True, slots=True)
class StrategyMetadata:
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
class ReasoningStrategy:
    strategy_type: StrategyType
    name: str
    description: str | None = None
    metadata: StrategyMetadata | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            object.__setattr__(self, "metadata", StrategyMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or StrategyMetadata()
        return {
            "strategy_type": self.strategy_type.value,
            "name": self.name,
            "description": self.description,
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ReasoningStrategyContract:
    supported_strategy_types: tuple[StrategyType, ...]
    metadata: StrategyMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supported_strategy_types",
            tuple(self.supported_strategy_types),
        )
        if self.metadata is None:
            object.__setattr__(self, "metadata", StrategyMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or StrategyMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_strategy_types": [
                strategy_type.value for strategy_type in self.supported_strategy_types
            ],
            "metadata": metadata.to_dict(),
        }


def validate_strategy_metadata(
    metadata: object,
    field_prefix: str = "strategy_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, StrategyMetadata):
        result.add_error(
            "Strategy metadata must be a StrategyMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_strategy_metadata",
        )

    return result


def validate_reasoning_strategy(
    strategy: object,
    field_prefix: str = "reasoning_strategy",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(strategy, ReasoningStrategy):
        result.add_error(
            "Reasoning strategy must be a ReasoningStrategy value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_strategy",
        )
        return result

    if not isinstance(strategy.strategy_type, StrategyType):
        result.add_error(
            "Reasoning strategy type must be a StrategyType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.strategy_type",
            code="invalid_strategy_type",
        )

    if not isinstance(strategy.name, str) or not strategy.name:
        result.add_error(
            "Reasoning strategy name must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.name",
            code="invalid_strategy_name",
        )

    if strategy.description is not None and not isinstance(strategy.description, str):
        result.add_error(
            "Reasoning strategy description must be a string when provided.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.description",
            code="invalid_strategy_description",
        )

    result.merge(validate_strategy_metadata(strategy.metadata, f"{field_prefix}.metadata"))

    return result


def validate_reasoning_strategy_contract(
    contract: object,
    field_prefix: str = "reasoning_strategy_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, ReasoningStrategyContract):
        result.add_error(
            "Reasoning strategy contract must be a ReasoningStrategyContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_strategy_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Reasoning strategy contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_reasoning_strategy_contract_version",
        )

    if not isinstance(contract.supported_strategy_types, tuple):
        result.add_error(
            "Supported strategy types must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_strategy_types",
            code="invalid_supported_strategy_types",
        )
    else:
        for index, strategy_type in enumerate(contract.supported_strategy_types):
            if not isinstance(strategy_type, StrategyType):
                result.add_error(
                    "Supported strategy types must be StrategyType values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_strategy_types[{index}]",
                    code="invalid_supported_strategy_type",
                )

    result.merge(validate_strategy_metadata(contract.metadata, f"{field_prefix}.metadata"))

    return result
