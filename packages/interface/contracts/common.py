from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import ValidationCategory, ValidationResult


class InterfaceResponseStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class InterfaceContractMetadata:
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
class InterfaceCorrelation:
    correlation_id: str
    trace_metadata: InterfaceContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.trace_metadata is None:
            object.__setattr__(self, "trace_metadata", InterfaceContractMetadata())

    def to_dict(self) -> dict[str, object]:
        trace_metadata = self.trace_metadata or InterfaceContractMetadata()
        return {
            "correlation_id": self.correlation_id,
            "trace_metadata": trace_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceOrigin:
    origin_identifier: str
    origin_metadata: InterfaceContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.origin_metadata is None:
            object.__setattr__(self, "origin_metadata", InterfaceContractMetadata())

    def to_dict(self) -> dict[str, object]:
        origin_metadata = self.origin_metadata or InterfaceContractMetadata()
        return {
            "origin_identifier": self.origin_identifier,
            "origin_metadata": origin_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceContextReference:
    reference_identifier: str
    reference_metadata: InterfaceContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.reference_metadata is None:
            object.__setattr__(self, "reference_metadata", InterfaceContractMetadata())

    def to_dict(self) -> dict[str, object]:
        reference_metadata = self.reference_metadata or InterfaceContractMetadata()
        return {
            "reference_identifier": self.reference_identifier,
            "reference_metadata": reference_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceContextReferenceCollection:
    references: tuple[InterfaceContextReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
        }


@dataclass(frozen=True, slots=True)
class CanonicalInterfacePayload:
    """Technology-neutral canonical payload container.

    Payload values are canonical data only. They SHALL NOT encode transport protocols,
    serialization formats, external providers, or execution environments.
    """

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
class InterfaceResponseResult:
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
class InterfaceResponseWarning:
    message: str
    warning_metadata: InterfaceContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.warning_metadata is None:
            object.__setattr__(self, "warning_metadata", InterfaceContractMetadata())

    def to_dict(self) -> dict[str, object]:
        warning_metadata = self.warning_metadata or InterfaceContractMetadata()
        return {
            "message": self.message,
            "warning_metadata": warning_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceResponseError:
    message: str
    error_metadata: InterfaceContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.error_metadata is None:
            object.__setattr__(self, "error_metadata", InterfaceContractMetadata())

    def to_dict(self) -> dict[str, object]:
        error_metadata = self.error_metadata or InterfaceContractMetadata()
        return {
            "message": self.message,
            "error_metadata": error_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceResponseErrorCollection:
    errors: tuple[InterfaceResponseError, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "errors", tuple(self.errors))

    def to_dict(self) -> dict[str, object]:
        return {
            "errors": [error.to_dict() for error in self.errors],
        }


def validate_interface_contract_metadata(
    metadata: object,
    field_prefix: str = "contract_metadata",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(metadata, InterfaceContractMetadata):
        result.add_error(
            "Contract metadata must be an InterfaceContractMetadata value.",
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


def validate_interface_correlation(
    correlation: object,
    field_prefix: str = "correlation",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(correlation, InterfaceCorrelation):
        result.add_error(
            "Correlation must be an InterfaceCorrelation value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_correlation",
        )
        return result

    if not isinstance(correlation.correlation_id, str) or not correlation.correlation_id:
        result.add_error(
            "Correlation identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.correlation_id",
            code="invalid_correlation_id",
        )

    trace_metadata = correlation.trace_metadata
    if trace_metadata is not None:
        result.merge(
            validate_interface_contract_metadata(
                trace_metadata,
                field_prefix=f"{field_prefix}.trace_metadata",
            )
        )

    return result


def validate_interface_origin(
    origin: object,
    field_prefix: str = "origin",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(origin, InterfaceOrigin):
        result.add_error(
            "Origin must be an InterfaceOrigin value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_origin",
        )
        return result

    if not isinstance(origin.origin_identifier, str) or not origin.origin_identifier:
        result.add_error(
            "Origin identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.origin_identifier",
            code="invalid_origin_identifier",
        )

    origin_metadata = origin.origin_metadata
    if origin_metadata is not None:
        result.merge(
            validate_interface_contract_metadata(
                origin_metadata,
                field_prefix=f"{field_prefix}.origin_metadata",
            )
        )

    return result


def validate_interface_context_reference(
    reference: object,
    field_prefix: str = "context_reference",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, InterfaceContextReference):
        result.add_error(
            "Context reference must be an InterfaceContextReference value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_context_reference",
        )
        return result

    if not isinstance(reference.reference_identifier, str) or not reference.reference_identifier:
        result.add_error(
            "Context reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.reference_identifier",
            code="invalid_context_reference_identifier",
        )

    reference_metadata = reference.reference_metadata
    if reference_metadata is not None:
        result.merge(
            validate_interface_contract_metadata(
                reference_metadata,
                field_prefix=f"{field_prefix}.reference_metadata",
            )
        )

    return result


def validate_interface_context_reference_collection(
    collection: object,
    field_prefix: str = "context_references",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, InterfaceContextReferenceCollection):
        result.add_error(
            "Context references must be an InterfaceContextReferenceCollection value.",
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
            validate_interface_context_reference(
                reference,
                field_prefix=f"{field_prefix}.references[{index}]",
            )
        )

    return result


def validate_canonical_interface_payload(
    payload: object,
    field_prefix: str = "canonical_payload",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(payload, CanonicalInterfacePayload):
        result.add_error(
            "Canonical payload must be a CanonicalInterfacePayload value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_canonical_payload",
        )
        return result

    if not isinstance(payload.values, tuple):
        result.add_error(
            "Canonical payload values must be stored as an immutable tuple.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.values",
            code="invalid_canonical_payload_values",
        )

    return result


def validate_interface_response_result(
    result_value: object,
    field_prefix: str = "result",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(result_value, InterfaceResponseResult):
        result.add_error(
            "Response result must be an InterfaceResponseResult value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_response_result",
        )
        return result

    if not isinstance(result_value.values, tuple):
        result.add_error(
            "Response result values must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.values",
            code="invalid_response_result_values",
        )

    return result


def validate_interface_response_warning(
    warning: object,
    field_prefix: str = "warning",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(warning, InterfaceResponseWarning):
        result.add_error(
            "Response warning must be an InterfaceResponseWarning value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_response_warning",
        )
        return result

    if not isinstance(warning.message, str) or not warning.message:
        result.add_error(
            "Response warning message must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.message",
            code="invalid_response_warning_message",
        )

    warning_metadata = warning.warning_metadata
    if warning_metadata is not None:
        result.merge(
            validate_interface_contract_metadata(
                warning_metadata,
                field_prefix=f"{field_prefix}.warning_metadata",
            )
        )

    return result


def validate_interface_response_error(
    error: object,
    field_prefix: str = "error",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(error, InterfaceResponseError):
        result.add_error(
            "Response error must be an InterfaceResponseError value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_response_error",
        )
        return result

    if not isinstance(error.message, str) or not error.message:
        result.add_error(
            "Response error message must be a non-empty string.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.message",
            code="invalid_response_error_message",
        )

    error_metadata = error.error_metadata
    if error_metadata is not None:
        result.merge(
            validate_interface_contract_metadata(
                error_metadata,
                field_prefix=f"{field_prefix}.error_metadata",
            )
        )

    return result


def validate_interface_response_error_collection(
    collection: object,
    field_prefix: str = "errors",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, InterfaceResponseErrorCollection):
        result.add_error(
            "Response errors must be an InterfaceResponseErrorCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_response_error_collection",
        )
        return result

    if not isinstance(collection.errors, tuple):
        result.add_error(
            "Response errors must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.errors",
            code="invalid_response_error_collection_errors",
        )
        return result

    for index, error in enumerate(collection.errors):
        result.merge(
            validate_interface_response_error(
                error,
                field_prefix=f"{field_prefix}.errors[{index}]",
            )
        )

    return result
