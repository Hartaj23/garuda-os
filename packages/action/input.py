from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class ActionInputType(StrEnum):
    MEMORY = "memory"
    KNOWLEDGE = "knowledge"
    CONTEXT = "context"
    REASONING = "reasoning"
    DECISION = "decision"
    EXTERNAL = "external"


@dataclass(frozen=True, slots=True)
class ActionInputReference:
    input_type: ActionInputType
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
class ActionInputCollection:
    references: tuple[ActionInputReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
        }


def validate_action_input_reference(
    reference: object,
    field_prefix: str = "action_input_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, ActionInputReference):
        result.add_error(
            "Action input reference must be an ActionInputReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_input_reference",
        )
        return result

    if not isinstance(reference.input_type, ActionInputType):
        result.add_error(
            "Action input type must be an ActionInputType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.input_type",
            code="invalid_action_input_type",
        )

    if not isinstance(reference.identifier, str) or not reference.identifier:
        result.add_error(
            "Action input identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.identifier",
            code="invalid_action_input_identifier",
        )

    if not isinstance(reference.reference_metadata, tuple):
        result.add_error(
            "Action input reference metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.reference_metadata",
            code="invalid_action_input_reference_metadata",
        )

    return result


def validate_action_input_collection(
    collection: object,
    field_prefix: str = "action_inputs",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, ActionInputCollection):
        result.add_error(
            "Action inputs must be an ActionInputCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_action_input_collection",
        )
        return result

    if not isinstance(collection.references, tuple):
        result.add_error(
            "Action input references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.references",
            code="invalid_action_input_references",
        )
        return result

    for index, reference in enumerate(collection.references):
        result.merge(
            validate_action_input_reference(
                reference,
                f"{field_prefix}.references[{index}]",
            )
        )

    return result
