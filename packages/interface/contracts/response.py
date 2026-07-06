from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import (
    InterfaceContractMetadata,
    InterfaceResponseErrorCollection,
    InterfaceResponseResult,
    InterfaceResponseStatus,
    InterfaceResponseWarning,
    validate_interface_contract_metadata,
    validate_interface_response_error_collection,
    validate_interface_response_result,
    validate_interface_response_warning,
)


class CanonicalInterfaceResponse(CanonicalObject):
    """Canonical response contract for communication across the Constitutional Membrane.

    Contract invariants:
    - Required fields: status, result, warnings, errors, contract_metadata
    - Optional fields: Platform Core constructor fields (object_id, metadata, tags, lifecycle, audit)
    - Immutable after construction: all contract-specific fields
    - Equality semantics: not overridden; identity follows object identity semantics
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full contract via to_dict()
    - Error semantics: warnings and errors define structure only — no taxonomy, codes, retry, or recovery
    """

    def __init__(
        self,
        status: InterfaceResponseStatus,
        result: InterfaceResponseResult,
        warnings: tuple[InterfaceResponseWarning, ...] = (),
        errors: InterfaceResponseErrorCollection | None = None,
        contract_metadata: InterfaceContractMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._status = status
        self._result = result
        self._warnings = tuple(warnings)
        self._errors = errors or InterfaceResponseErrorCollection()
        self._contract_metadata = contract_metadata or InterfaceContractMetadata()
        self.register_validation_hook(validate_canonical_interface_response)

    @property
    def status(self) -> InterfaceResponseStatus:
        return self._status

    @property
    def result(self) -> InterfaceResponseResult:
        return self._result

    @property
    def warnings(self) -> tuple[InterfaceResponseWarning, ...]:
        return self._warnings

    @property
    def errors(self) -> InterfaceResponseErrorCollection:
        return self._errors

    @property
    def contract_metadata(self) -> InterfaceContractMetadata:
        return self._contract_metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "object_version": self.object_version,
            "object_type": self.object_type,
            "object_id": str(self.object_id),
            "metadata": dict(sorted(self.metadata.values.items())),
            "tags": list(self.tags),
            "lifecycle_state": self.lifecycle_state.value,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "result": self.result.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
            "errors": self.errors.to_dict()["errors"],
            "contract_metadata": self.contract_metadata.to_dict(),
        }


def validate_canonical_interface_response(obj: CanonicalInterfaceResponse) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "status", None), InterfaceResponseStatus):
        result.add_error(
            "Response status must be an InterfaceResponseStatus value.",
            ValidationCategory.SCHEMA,
            field="status",
            code="invalid_response_status",
        )

    response_result = getattr(obj, "result", None)
    if not isinstance(response_result, InterfaceResponseResult):
        result.add_error(
            "Response result must be an InterfaceResponseResult value.",
            ValidationCategory.METADATA,
            field="result",
            code="invalid_response_result",
        )
    else:
        result.merge(validate_interface_response_result(response_result))

    warnings = getattr(obj, "warnings", None)
    if not isinstance(warnings, tuple):
        result.add_error(
            "Response warnings must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="warnings",
            code="invalid_response_warnings",
        )
    else:
        for index, warning in enumerate(warnings):
            result.merge(
                validate_interface_response_warning(
                    warning,
                    field_prefix=f"warnings[{index}]",
                )
            )

    response_errors = getattr(obj, "errors", None)
    if not isinstance(response_errors, InterfaceResponseErrorCollection):
        result.add_error(
            "Response errors must be an InterfaceResponseErrorCollection value.",
            ValidationCategory.METADATA,
            field="errors",
            code="invalid_response_errors",
        )
    else:
        result.merge(validate_interface_response_error_collection(response_errors))

    contract_metadata = getattr(obj, "contract_metadata", None)
    if not isinstance(contract_metadata, InterfaceContractMetadata):
        result.add_error(
            "Contract metadata must be an InterfaceContractMetadata value.",
            ValidationCategory.METADATA,
            field="contract_metadata",
            code="invalid_contract_metadata",
        )
    else:
        result.merge(validate_interface_contract_metadata(contract_metadata))

    return result
