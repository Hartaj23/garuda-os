from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult

from .input import DecisionInputReference, validate_decision_input_reference


class DecisionOrigin(StrEnum):
    HUMAN = "human"
    AUTOMATED = "automated"
    IMPORTED = "imported"
    EXTERNAL = "external"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DecisionProvenance:
    origin: DecisionOrigin
    author: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    input_references: tuple[DecisionInputReference, ...] = ()
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
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "input_references": [
                reference.to_dict() for reference in self.input_references
            ],
            "provenance_metadata": dict(self.provenance_metadata),
        }


def validate_decision_provenance(
    provenance: object,
    field_prefix: str = "decision_provenance",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(provenance, DecisionProvenance):
        result.add_error(
            "Decision provenance must be a DecisionProvenance value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_decision_provenance",
        )
        return result

    if not isinstance(provenance.origin, DecisionOrigin):
        result.add_error(
            "Decision provenance origin must be a DecisionOrigin value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.origin",
            code="invalid_decision_origin",
        )

    if provenance.author is not None and not isinstance(provenance.author, str):
        result.add_error(
            "Decision provenance author must be a string when provided.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.author",
            code="invalid_decision_provenance_author",
        )

    if not hasattr(provenance.created_at, "isoformat"):
        result.add_error(
            "Decision provenance timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.created_at",
            code="invalid_decision_provenance_created_at",
        )

    if not isinstance(provenance.input_references, tuple):
        result.add_error(
            "Decision provenance input references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.input_references",
            code="invalid_decision_provenance_input_references",
        )
    else:
        for index, reference in enumerate(provenance.input_references):
            result.merge(
                validate_decision_input_reference(
                    reference,
                    f"{field_prefix}.input_references[{index}]",
                )
            )

    if not isinstance(provenance.provenance_metadata, tuple):
        result.add_error(
            "Decision provenance metadata must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.provenance_metadata",
            code="invalid_decision_provenance_metadata",
        )

    return result
