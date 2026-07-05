from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class DecisionStrategyType(StrEnum):
    ANALYTICAL = "analytical"
    HEURISTIC = "heuristic"
    RULE_BASED = "rule_based"
    CONSENSUS = "consensus"
    EXPERT = "expert"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DecisionStrategyMetadata:
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
class DecisionStrategy:
    strategy_type: DecisionStrategyType
    name: str
    description: str | None = None
    metadata: DecisionStrategyMetadata | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            object.__setattr__(self, "metadata", DecisionStrategyMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or DecisionStrategyMetadata()
        return {
            "strategy_type": self.strategy_type.value,
            "name": self.name,
            "description": self.description,
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class DecisionStrategyContract:
    strategies: tuple[DecisionStrategy, ...]
    metadata: DecisionStrategyMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "strategies", tuple(self.strategies))
        if self.metadata is None:
            object.__setattr__(self, "metadata", DecisionStrategyMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or DecisionStrategyMetadata()
        return {
            "contract_version": self.contract_version,
            "strategies": [strategy.to_dict() for strategy in self.strategies],
            "metadata": metadata.to_dict(),
        }


def validate_decision_strategy_metadata(
    metadata: object,
    field_prefix: str = "decision_strategy_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, DecisionStrategyMetadata):
        result.add_error(
            "Decision strategy metadata must be a DecisionStrategyMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_strategy_metadata",
        )

    return result


def validate_decision_strategy(
    strategy: object,
    field_prefix: str = "decision_strategy",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(strategy, DecisionStrategy):
        result.add_error(
            "Decision strategy must be a DecisionStrategy value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_strategy",
        )
        return result

    if not isinstance(strategy.strategy_type, DecisionStrategyType):
        result.add_error(
            "Decision strategy type must be a DecisionStrategyType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.strategy_type",
            code="invalid_decision_strategy_type",
        )

    if not isinstance(strategy.name, str) or not strategy.name:
        result.add_error(
            "Decision strategy name must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.name",
            code="invalid_decision_strategy_name",
        )

    if strategy.description is not None and not isinstance(strategy.description, str):
        result.add_error(
            "Decision strategy description must be a string when provided.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.description",
            code="invalid_decision_strategy_description",
        )

    result.merge(
        validate_decision_strategy_metadata(
            strategy.metadata,
            f"{field_prefix}.metadata",
        )
    )

    return result


def validate_decision_strategy_contract(
    contract: object,
    field_prefix: str = "decision_strategy_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, DecisionStrategyContract):
        result.add_error(
            "Decision strategy contract must be a DecisionStrategyContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_strategy_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Decision strategy contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_decision_strategy_contract_version",
        )

    if not isinstance(contract.strategies, tuple):
        result.add_error(
            "Decision strategy contract strategies must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.strategies",
            code="invalid_decision_strategy_contract_strategies",
        )
    elif not contract.strategies:
        result.add_error(
            "Decision strategy contract must contain at least one strategy.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.strategies",
            code="empty_decision_strategy_contract_strategies",
        )
    else:
        for index, strategy in enumerate(contract.strategies):
            result.merge(
                validate_decision_strategy(
                    strategy,
                    f"{field_prefix}.strategies[{index}]",
                )
            )

    result.merge(
        validate_decision_strategy_metadata(
            contract.metadata,
            f"{field_prefix}.metadata",
        )
    )

    return result
