from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


@dataclass(frozen=True, slots=True)
class RuntimeContractMetadata:
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
class RuntimeContextReference:
    """Technology-neutral runtime context reference."""

    context_identifier: str
    context_metadata: RuntimeContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.context_metadata is None:
            object.__setattr__(self, "context_metadata", RuntimeContractMetadata())

    def to_dict(self) -> dict[str, object]:
        context_metadata = self.context_metadata or RuntimeContractMetadata()
        return {
            "context_identifier": self.context_identifier,
            "context_metadata": context_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class RuntimeContextReferenceCollection:
    references: tuple[RuntimeContextReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
        }


def validate_runtime_contract_metadata(
    metadata: object,
    field_prefix: str = "contract_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, RuntimeContractMetadata):
        result.add_error(
            "Contract metadata must be a RuntimeContractMetadata value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_contract_metadata",
        )
        return result

    if not isinstance(metadata.values, tuple):
        result.add_error(
            "Contract metadata values must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.values",
            code="invalid_contract_metadata_values",
        )

    return result


def validate_runtime_context_reference(
    reference: object,
    field_prefix: str = "context_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, RuntimeContextReference):
        result.add_error(
            "Context reference must be a RuntimeContextReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_reference",
        )
        return result

    if not isinstance(reference.context_identifier, str) or not reference.context_identifier:
        result.add_error(
            "Context identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.context_identifier",
            code="invalid_context_identifier",
        )

    context_metadata = reference.context_metadata
    if context_metadata is not None:
        result.merge(
            validate_runtime_contract_metadata(
                context_metadata,
                field_prefix=f"{field_prefix}.context_metadata",
            )
        )

    return result


def validate_runtime_context_reference_collection(
    collection: object,
    field_prefix: str = "context_references",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, RuntimeContextReferenceCollection):
        result.add_error(
            "Context references must be a RuntimeContextReferenceCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_reference_collection",
        )
        return result

    if not isinstance(collection.references, tuple):
        result.add_error(
            "Context references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.references",
            code="invalid_context_reference_collection_references",
        )
        return result

    for index, reference in enumerate(collection.references):
        result.merge(
            validate_runtime_context_reference(
                reference,
                field_prefix=f"{field_prefix}.references[{index}]",
            )
        )

    return result
