from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class ActionChainType(StrEnum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DEPENDENCY = "dependency"
    REVIEW = "review"
    FALLBACK = "fallback"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ActionChainMetadata:
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
class ActionStepReference:
    action_identifier: str
    metadata: ActionChainMetadata | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            object.__setattr__(self, "metadata", ActionChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ActionChainMetadata()
        return {
            "action_identifier": self.action_identifier,
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ActionChain:
    chain_type: ActionChainType
    steps: tuple[ActionStepReference, ...] = ()
    metadata: ActionChainMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))
        if self.metadata is None:
            object.__setattr__(self, "metadata", ActionChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ActionChainMetadata()
        return {
            "chain_type": self.chain_type.value,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ActionChainContract:
    chains: tuple[ActionChain, ...]
    metadata: ActionChainMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(self, "chains", tuple(self.chains))
        if self.metadata is None:
            object.__setattr__(self, "metadata", ActionChainMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.metadata or ActionChainMetadata()
        return {
            "contract_version": self.contract_version,
            "chains": [chain.to_dict() for chain in self.chains],
            "metadata": metadata.to_dict(),
        }


def validate_action_chain_metadata(
    metadata: object,
    field_prefix: str = "action_chain_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, ActionChainMetadata):
        result.add_error(
            "Action chain metadata must be an ActionChainMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_chain_metadata",
        )

    return result


def validate_action_step_reference(
    step: object,
    field_prefix: str = "action_step_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(step, ActionStepReference):
        result.add_error(
            "Action step reference must be an ActionStepReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_step_reference",
        )
        return result

    if not isinstance(step.action_identifier, str) or not step.action_identifier:
        result.add_error(
            "Action step reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.action_identifier",
            code="invalid_action_step_identifier",
        )

    result.merge(
        validate_action_chain_metadata(
            step.metadata,
            f"{field_prefix}.metadata",
        )
    )

    return result


def validate_action_chain(
    chain: object,
    field_prefix: str = "action_chain",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(chain, ActionChain):
        result.add_error(
            "Action chain must be an ActionChain value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_chain",
        )
        return result

    if not isinstance(chain.chain_type, ActionChainType):
        result.add_error(
            "Action chain type must be an ActionChainType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.chain_type",
            code="invalid_action_chain_type",
        )

    if not isinstance(chain.steps, tuple):
        result.add_error(
            "Action chain steps must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.steps",
            code="invalid_action_chain_steps",
        )
    else:
        for index, step in enumerate(chain.steps):
            result.merge(
                validate_action_step_reference(
                    step,
                    f"{field_prefix}.steps[{index}]",
                )
            )

    result.merge(validate_action_chain_metadata(chain.metadata, f"{field_prefix}.metadata"))

    return result


def validate_action_chain_contract(
    contract: object,
    field_prefix: str = "action_chain_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, ActionChainContract):
        result.add_error(
            "Action chain contract must be an ActionChainContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_chain_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Action chain contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_action_chain_contract_version",
        )

    if not isinstance(contract.chains, tuple):
        result.add_error(
            "Action chain contract chains must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.chains",
            code="invalid_action_chain_contract_chains",
        )
    elif not contract.chains:
        result.add_error(
            "Action chain contract must contain at least one chain.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.chains",
            code="empty_action_chain_contract_chains",
        )
    else:
        for index, chain in enumerate(contract.chains):
            result.merge(
                validate_action_chain(
                    chain,
                    f"{field_prefix}.chains[{index}]",
                )
            )

    result.merge(
        validate_action_chain_metadata(
            contract.metadata,
            f"{field_prefix}.metadata",
        )
    )

    return result
