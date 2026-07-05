from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult

from .input import ReasoningInputReference, validate_reasoning_input_reference


class ReasoningOrigin(StrEnum):
    HUMAN_DEFINED = "human_defined"
    SYSTEM_GENERATED = "system_generated"
    IMPORTED = "imported"
    VALIDATED = "validated"
    DERIVED = "derived"


@dataclass(frozen=True, slots=True)
class ReasoningProvenance:
    origin: ReasoningOrigin
    creator: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    input_references: tuple[ReasoningInputReference, ...] = ()
    provenance_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "input_references", tuple(self.input_references))
        if isinstance(self.provenance_metadata, dict):
            object.__setattr__(
                self,
                "provenance_metadata",
                tuple(sorted(self.provenance_metadata.items())),
            )
        elif isinstance(self.provenance_metadata, tuple):
            object.__setattr__(
                self,
                "provenance_metadata",
                tuple(sorted(self.provenance_metadata)),
            )
        else:
            raise ValueError("provenance_metadata must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, object]:
        return {
            "origin": self.origin.value,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "input_references": [
                reference.to_dict() for reference in self.input_references
            ],
            "provenance_metadata": dict(self.provenance_metadata),
        }


def validate_reasoning_provenance(
    provenance: object,
    field_prefix: str = "reasoning_provenance",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(provenance, ReasoningProvenance):
        result.add_error(
            "Reasoning provenance must be a ReasoningProvenance value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reasoning_provenance",
        )
        return result

    if not isinstance(provenance.origin, ReasoningOrigin):
        result.add_error(
            "Reasoning provenance origin must be a ReasoningOrigin value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.origin",
            code="invalid_reasoning_origin",
        )

    if not hasattr(provenance.created_at, "isoformat"):
        result.add_error(
            "Reasoning provenance timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.created_at",
            code="invalid_reasoning_provenance_created_at",
        )

    if not isinstance(provenance.input_references, tuple):
        result.add_error(
            "Reasoning provenance input references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.input_references",
            code="invalid_reasoning_provenance_input_references",
        )
    else:
        for index, reference in enumerate(provenance.input_references):
            result.merge(
                validate_reasoning_input_reference(
                    reference,
                    f"{field_prefix}.input_references[{index}]",
                )
            )

    if not isinstance(provenance.provenance_metadata, tuple):
        result.add_error(
            "Reasoning provenance metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.provenance_metadata",
            code="invalid_reasoning_provenance_metadata",
        )

    return result
