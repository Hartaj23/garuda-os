from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult

from .metadata import TranslationMetadata, validate_translation_metadata


class ExternalRepresentationKind(StrEnum):
    UNSPECIFIED = "unspecified"
    STRUCTURED = "structured"
    OPAQUE = "opaque"


@dataclass(frozen=True, slots=True)
class ExternalRepresentation:
    """Technology-neutral opaque external representation container.

    External representations are treated as opaque architectural descriptions.
    They do not expose or imply protocol semantics, serialization formats,
    transport characteristics, or provider identity.
    """

    representation_kind: ExternalRepresentationKind
    representation_identifier: str
    representation_values: dict[str, Any] | tuple[tuple[str, Any], ...] = field(
        default_factory=tuple
    )
    representation_metadata: TranslationMetadata | None = None

    def __post_init__(self) -> None:
        if isinstance(self.representation_values, dict):
            object.__setattr__(
                self,
                "representation_values",
                tuple(sorted(self.representation_values.items())),
            )
        elif isinstance(self.representation_values, tuple):
            object.__setattr__(
                self,
                "representation_values",
                tuple(sorted(self.representation_values)),
            )
        else:
            raise ValueError(
                "representation_values must be a dictionary or tuple of key-value pairs"
            )
        if self.representation_metadata is None:
            object.__setattr__(self, "representation_metadata", TranslationMetadata())

    def to_dict(self) -> dict[str, object]:
        representation_metadata = self.representation_metadata or TranslationMetadata()
        return {
            "representation_kind": self.representation_kind.value,
            "representation_identifier": self.representation_identifier,
            "representation_values": dict(self.representation_values),
            "representation_metadata": representation_metadata.to_dict(),
        }


def validate_external_representation(
    representation: object,
    field_prefix: str = "source_representation",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(representation, ExternalRepresentation):
        result.add_error(
            "External representation must be an ExternalRepresentation value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_external_representation",
        )
        return result

    if not isinstance(representation.representation_kind, ExternalRepresentationKind):
        result.add_error(
            "Representation kind must be an ExternalRepresentationKind value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.representation_kind",
            code="invalid_representation_kind",
        )

    if (
        not isinstance(representation.representation_identifier, str)
        or not representation.representation_identifier
    ):
        result.add_error(
            "Representation identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.representation_identifier",
            code="invalid_representation_identifier",
        )

    if not isinstance(representation.representation_values, tuple):
        result.add_error(
            "Representation values must be stored as an immutable tuple.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.representation_values",
            code="invalid_representation_values",
        )

    representation_metadata = representation.representation_metadata
    if representation_metadata is not None:
        result.merge(
            validate_translation_metadata(
                representation_metadata,
                field_prefix=f"{field_prefix}.representation_metadata",
            )
        )

    return result
