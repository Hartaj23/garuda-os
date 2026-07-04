from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class CompositionType(StrEnum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    LAYERED = "layered"
    HIERARCHICAL = "hierarchical"
    GROUPED = "grouped"


@dataclass(frozen=True, slots=True)
class CompositionMetadata:
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
class ContextComposition:
    composition_type: CompositionType
    context_identifiers: tuple[str, ...]
    composition_metadata: CompositionMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "context_identifiers", tuple(self.context_identifiers))
        if self.composition_metadata is None:
            object.__setattr__(self, "composition_metadata", CompositionMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.composition_metadata or CompositionMetadata()
        return {
            "composition_type": self.composition_type.value,
            "context_identifiers": list(self.context_identifiers),
            "composition_metadata": metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ContextCompositionContract:
    supported_composition_types: tuple[CompositionType, ...]
    supported_metadata: CompositionMetadata | None = None
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supported_composition_types",
            tuple(self.supported_composition_types),
        )
        if self.supported_metadata is None:
            object.__setattr__(self, "supported_metadata", CompositionMetadata())

    def to_dict(self) -> dict[str, object]:
        metadata = self.supported_metadata or CompositionMetadata()
        return {
            "contract_version": self.contract_version,
            "supported_composition_types": [
                composition_type.value
                for composition_type in self.supported_composition_types
            ],
            "supported_metadata": metadata.to_dict(),
        }


def validate_composition_metadata(
    metadata: object,
    field_prefix: str = "composition_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, CompositionMetadata):
        result.add_error(
            "Composition metadata must be a CompositionMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_composition_metadata",
        )

    return result


def validate_context_composition(
    composition: object,
    field_prefix: str = "context_composition",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(composition, ContextComposition):
        result.add_error(
            "Context composition must be a ContextComposition value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_composition",
        )
        return result

    if not isinstance(composition.composition_type, CompositionType):
        result.add_error(
            "Context composition type must be a CompositionType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.composition_type",
            code="invalid_composition_type",
        )

    if not isinstance(composition.context_identifiers, tuple):
        result.add_error(
            "Context composition identifiers must be stored as an immutable tuple.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.context_identifiers",
            code="invalid_context_identifiers",
        )
    else:
        for index, identifier in enumerate(composition.context_identifiers):
            if not isinstance(identifier, str) or not identifier:
                result.add_error(
                    "Context composition identifiers must be non-empty strings.",
                    ValidationCategory.IDENTITY,
                    field=f"{field_prefix}.context_identifiers[{index}]",
                    code="invalid_context_identifier",
                )

    result.merge(
        validate_composition_metadata(
            composition.composition_metadata,
            f"{field_prefix}.composition_metadata",
        )
    )

    return result


def validate_context_composition_contract(
    contract: object,
    field_prefix: str = "composition_contract",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(contract, ContextCompositionContract):
        result.add_error(
            "Context composition contract must be a ContextCompositionContract value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_composition_contract",
        )
        return result

    if not isinstance(contract.contract_version, str) or not contract.contract_version:
        result.add_error(
            "Context composition contract version must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.contract_version",
            code="invalid_context_composition_contract_version",
        )

    if not isinstance(contract.supported_composition_types, tuple):
        result.add_error(
            "Supported composition types must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.supported_composition_types",
            code="invalid_supported_composition_types",
        )
    else:
        for index, composition_type in enumerate(contract.supported_composition_types):
            if not isinstance(composition_type, CompositionType):
                result.add_error(
                    "Supported composition types must be CompositionType values.",
                    ValidationCategory.METADATA,
                    field=f"{field_prefix}.supported_composition_types[{index}]",
                    code="invalid_supported_composition_type",
                )

    result.merge(
        validate_composition_metadata(
            contract.supported_metadata,
            f"{field_prefix}.supported_metadata",
        )
    )

    return result
