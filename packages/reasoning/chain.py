from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class ChainType(StrEnum):
    LINEAR = "linear"
    BRANCHING = "branching"
    HIERARCHICAL = "hierarchical"
    DEPENDENCY = "dependency"
    COMPARATIVE = "comparative"


@dataclass(frozen=True, slots=True)
class ChainMetadata:
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
class ReasoningStepReference:
    identifier: str
    sequence: int
    metadata: ChainMetadata | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            object.__setattr__(self, "metadata", ChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ChainMetadata()
        return {
            "identifier": self.identifier,
            "sequence": self.sequence,
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ReasoningChain:
    chain_type: ChainType
    steps: tuple[ReasoningStepReference, ...] = ()
    metadata: ChainMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))
        if self.metadata is None:
            object.__setattr__(self, "metadata", ChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ChainMetadata()
        return {
            "chain_type": self.chain_type.value,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ReasoningChainContract:
    supported_chain_types: tuple[ChainType, ...]
    metadata: ChainMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supported_chain_types",
            tuple(self.supported_chain_types),
        )
        if self.metadata is None:
            object.__setattr__(self, "metadata", ChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ChainMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_chain_types": [
                chain_type.value for chain_type in self.supported_chain_types
            ],
            "metadata": metadata.to_dict(),
        }


def validate_chain_metadata(
    metadata: object,
    field_prefix: str = "chain_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, ChainMetadata):
        result.add_error(
            "Chain metadata must be a ChainMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_chain_metadata",
        )

    return result


def validate_reasoning_step_reference(
    step: object,
    field_prefix: str = "reasoning_step_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(step, ReasoningStepReference):
        result.add_error(
            "Reasoning step reference must be a ReasoningStepReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_step_reference",
        )
        return result

    if not isinstance(step.identifier, str) or not step.identifier:
        result.add_error(
            "Reasoning step reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.identifier",
            code="invalid_reasoning_step_identifier",
        )

    if not isinstance(step.sequence, int) or step.sequence < 0:
        result.add_error(
            "Reasoning step reference sequence must be a non-negative integer.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.sequence",
            code="invalid_reasoning_step_sequence",
        )

    result.merge(validate_chain_metadata(step.metadata, f"{field_prefix}.metadata"))

    return result


def validate_reasoning_chain(
    chain: object,
    field_prefix: str = "reasoning_chain",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(chain, ReasoningChain):
        result.add_error(
            "Reasoning chain must be a ReasoningChain value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_chain",
        )
        return result

    if not isinstance(chain.chain_type, ChainType):
        result.add_error(
            "Reasoning chain type must be a ChainType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.chain_type",
            code="invalid_chain_type",
        )

    if not isinstance(chain.steps, tuple):
        result.add_error(
            "Reasoning chain steps must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.steps",
            code="invalid_reasoning_chain_steps",
        )
    else:
        for index, step in enumerate(chain.steps):
            result.merge(
                validate_reasoning_step_reference(
                    step,
                    f"{field_prefix}.steps[{index}]",
                )
            )

    result.merge(validate_chain_metadata(chain.metadata, f"{field_prefix}.metadata"))

    return result


def validate_reasoning_chain_contract(
    contract: object,
    field_prefix: str = "reasoning_chain_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, ReasoningChainContract):
        result.add_error(
            "Reasoning chain contract must be a ReasoningChainContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_chain_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Reasoning chain contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_reasoning_chain_contract_version",
        )

    if not isinstance(contract.supported_chain_types, tuple):
        result.add_error(
            "Supported chain types must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_chain_types",
            code="invalid_supported_chain_types",
        )
    else:
        for index, chain_type in enumerate(contract.supported_chain_types):
            if not isinstance(chain_type, ChainType):
                result.add_error(
                    "Supported chain types must be ChainType values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_chain_types[{index}]",
                    code="invalid_supported_chain_type",
                )

    result.merge(validate_chain_metadata(contract.metadata, f"{field_prefix}.metadata"))

    return result
