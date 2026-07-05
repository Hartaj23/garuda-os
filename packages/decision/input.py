from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class DecisionInputType(StrEnum):
    KNOWLEDGE = "knowledge"
    CONTEXT = "context"
    REASONING = "reasoning"
    MEMORY = "memory"
    EXTERNAL = "external"


@dataclass(frozen=True, slots=True)
class DecisionInputReference:
    input_type: DecisionInputType
    identifier: str
    reference_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.reference_metadata, dict):
            object.__setattr__(
                self,
                "reference_metadata",
                tuple(sorted(self.reference_metadata.items())),
            )
        elif isinstance(self.reference_metadata, tuple):
            object.__setattr__(
                self,
                "reference_metadata",
                tuple(sorted(self.reference_metadata)),
            )
        else:
            raise ValueError("reference_metadata must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, object]:
        return {
            "input_type": self.input_type.value,
            "identifier": self.identifier,
            "reference_metadata": dict(self.reference_metadata),
        }


@dataclass(frozen=True, slots=True)
class DecisionInputCollection:
    references: tuple[DecisionInputReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
        }


def validate_decision_input_reference(
    reference: object,
    field_prefix: str = "decision_input_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, DecisionInputReference):
        result.add_error(
            "Decision input reference must be a DecisionInputReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_input_reference",
        )
        return result

    if not isinstance(reference.input_type, DecisionInputType):
        result.add_error(
            "Decision input type must be a DecisionInputType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.input_type",
            code="invalid_decision_input_type",
        )

    if not isinstance(reference.identifier, str) or not reference.identifier:
        result.add_error(
            "Decision input identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.identifier",
            code="invalid_decision_input_identifier",
        )

    if not isinstance(reference.reference_metadata, tuple):
        result.add_error(
            "Decision input reference metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.reference_metadata",
            code="invalid_decision_input_reference_metadata",
        )

    return result


def validate_decision_input_collection(
    collection: object,
    field_prefix: str = "decision_inputs",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, DecisionInputCollection):
        result.add_error(
            "Decision inputs must be a DecisionInputCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_input_collection",
        )
        return result

    if not isinstance(collection.references, tuple):
        result.add_error(
            "Decision input references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.references",
            code="invalid_decision_input_references",
        )
        return result

    for index, reference in enumerate(collection.references):
        result.merge(
            validate_decision_input_reference(
                reference,
                f"{field_prefix}.references[{index}]",
            )
        )

    return result
