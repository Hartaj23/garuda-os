from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from packages.objects import ValidationCategory, ValidationResult

from .metadata import TranslationMetadata, validate_translation_metadata


class TranslationDirection(StrEnum):
    INBOUND_TO_CANONICAL = "inbound_to_canonical"


@dataclass(frozen=True, slots=True)
class TranslationReversibilityDescriptor:
    """Records architectural reversibility, not operational reversibility.

    The descriptor records whether sufficient canonical information has been
    preserved to permit a future authorized reverse translation implementation.
    It does not imply that reverse translation exists.
    """

    preservation_complete: bool = True
    preserved_field_identifiers: tuple[str, ...] = ()
    reversibility_metadata: TranslationMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "preserved_field_identifiers", tuple(self.preserved_field_identifiers))
        if self.reversibility_metadata is None:
            object.__setattr__(self, "reversibility_metadata", TranslationMetadata())

    def to_dict(self) -> dict[str, object]:
        reversibility_metadata = self.reversibility_metadata or TranslationMetadata()
        return {
            "preservation_complete": self.preservation_complete,
            "preserved_field_identifiers": list(self.preserved_field_identifiers),
            "reversibility_metadata": reversibility_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class TranslationDescriptor:
    translation_direction: TranslationDirection
    source_representation_identifier: str
    target_payload_schema_identifier: str
    translation_metadata: TranslationMetadata | None = None
    reversibility: TranslationReversibilityDescriptor | None = None

    def __post_init__(self) -> None:
        if self.translation_metadata is None:
            object.__setattr__(self, "translation_metadata", TranslationMetadata())
        if self.reversibility is None:
            object.__setattr__(self, "reversibility", TranslationReversibilityDescriptor())

    def to_dict(self) -> dict[str, object]:
        translation_metadata = self.translation_metadata or TranslationMetadata()
        reversibility = self.reversibility or TranslationReversibilityDescriptor()
        return {
            "translation_direction": self.translation_direction.value,
            "source_representation_identifier": self.source_representation_identifier,
            "target_payload_schema_identifier": self.target_payload_schema_identifier,
            "translation_metadata": translation_metadata.to_dict(),
            "reversibility": reversibility.to_dict(),
        }


def validate_translation_reversibility_descriptor(
    descriptor: object,
    field_prefix: str = "reversibility",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, TranslationReversibilityDescriptor):
        result.add_error(
            "Reversibility descriptor must be a TranslationReversibilityDescriptor value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_reversibility_descriptor",
        )
        return result

    if not isinstance(descriptor.preserved_field_identifiers, tuple):
        result.add_error(
            "Preserved field identifiers must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.preserved_field_identifiers",
            code="invalid_preserved_field_identifiers",
        )

    reversibility_metadata = descriptor.reversibility_metadata
    if reversibility_metadata is not None:
        result.merge(
            validate_translation_metadata(
                reversibility_metadata,
                field_prefix=f"{field_prefix}.reversibility_metadata",
            )
        )

    return result


def validate_translation_descriptor(
    descriptor: object,
    field_prefix: str = "translation_descriptor",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(descriptor, TranslationDescriptor):
        result.add_error(
            "Translation descriptor must be a TranslationDescriptor value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_translation_descriptor",
        )
        return result

    if descriptor.translation_direction is not TranslationDirection.INBOUND_TO_CANONICAL:
        result.add_error(
            "Mission Delta supports inbound-to-canonical translation only.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.translation_direction",
            code="invalid_translation_direction",
        )

    if (
        not isinstance(descriptor.source_representation_identifier, str)
        or not descriptor.source_representation_identifier
    ):
        result.add_error(
            "Source representation identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.source_representation_identifier",
            code="invalid_source_representation_identifier",
        )

    if (
        not isinstance(descriptor.target_payload_schema_identifier, str)
        or not descriptor.target_payload_schema_identifier
    ):
        result.add_error(
            "Target payload schema identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.target_payload_schema_identifier",
            code="invalid_target_payload_schema_identifier",
        )

    translation_metadata = descriptor.translation_metadata
    if translation_metadata is not None:
        result.merge(
            validate_translation_metadata(
                translation_metadata,
                field_prefix=f"{field_prefix}.translation_metadata",
            )
        )

    reversibility = descriptor.reversibility
    if reversibility is not None:
        result.merge(
            validate_translation_reversibility_descriptor(
                reversibility,
                field_prefix=f"{field_prefix}.reversibility",
            )
        )

    return result
