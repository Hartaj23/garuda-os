from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import (
    CanonicalInterfacePayload,
    InterfaceContextReferenceCollection,
    InterfaceContractMetadata,
    InterfaceCorrelation,
    InterfaceOrigin,
    validate_canonical_interface_payload,
    validate_interface_context_reference_collection,
    validate_interface_contract_metadata,
    validate_interface_correlation,
    validate_interface_origin,
)


class CanonicalInterfaceRequest(CanonicalObject):
    """Canonical request contract for communication across the Constitutional Membrane.

    Contract invariants:
    - Required fields: contract_metadata, correlation, origin, context_references, canonical_payload
    - Optional fields: Platform Core constructor fields (object_id, metadata, tags, lifecycle, audit)
    - Immutable after construction: all contract-specific fields
    - Equality semantics: not overridden; identity follows object identity semantics
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full contract via to_dict()
    """

    def __init__(
        self,
        contract_metadata: InterfaceContractMetadata,
        correlation: InterfaceCorrelation,
        origin: InterfaceOrigin,
        context_references: InterfaceContextReferenceCollection,
        canonical_payload: CanonicalInterfacePayload,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._contract_metadata = contract_metadata
        self._correlation = correlation
        self._origin = origin
        self._context_references = context_references
        self._canonical_payload = canonical_payload
        self.register_validation_hook(validate_canonical_interface_request)

    @property
    def contract_metadata(self) -> InterfaceContractMetadata:
        return self._contract_metadata

    @property
    def correlation(self) -> InterfaceCorrelation:
        return self._correlation

    @property
    def origin(self) -> InterfaceOrigin:
        return self._origin

    @property
    def context_references(self) -> InterfaceContextReferenceCollection:
        return self._context_references

    @property
    def canonical_payload(self) -> CanonicalInterfacePayload:
        return self._canonical_payload

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
            "contract_metadata": self.contract_metadata.to_dict(),
            "correlation": self.correlation.to_dict(),
            "origin": self.origin.to_dict(),
            "context_references": self.context_references.to_dict(),
            "canonical_payload": self.canonical_payload.to_dict(),
        }


def validate_canonical_interface_request(obj: CanonicalInterfaceRequest) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "contract_metadata", None), InterfaceContractMetadata):
        result.add_error(
            "Contract metadata must be an InterfaceContractMetadata value.",
            ValidationCategory.METADATA,
            field="contract_metadata",
            code="invalid_contract_metadata",
        )
    else:
        result.merge(validate_interface_contract_metadata(obj.contract_metadata))

    if not isinstance(getattr(obj, "correlation", None), InterfaceCorrelation):
        result.add_error(
            "Correlation must be an InterfaceCorrelation value.",
            ValidationCategory.METADATA,
            field="correlation",
            code="invalid_correlation",
        )
    else:
        result.merge(validate_interface_correlation(obj.correlation))

    if not isinstance(getattr(obj, "origin", None), InterfaceOrigin):
        result.add_error(
            "Origin must be an InterfaceOrigin value.",
            ValidationCategory.METADATA,
            field="origin",
            code="invalid_origin",
        )
    else:
        result.merge(validate_interface_origin(obj.origin))

    context_references = getattr(obj, "context_references", None)
    if not isinstance(context_references, InterfaceContextReferenceCollection):
        result.add_error(
            "Context references must be an InterfaceContextReferenceCollection value.",
            ValidationCategory.METADATA,
            field="context_references",
            code="invalid_context_references",
        )
    else:
        result.merge(validate_interface_context_reference_collection(context_references))

    canonical_payload = getattr(obj, "canonical_payload", None)
    if not isinstance(canonical_payload, CanonicalInterfacePayload):
        result.add_error(
            "Canonical payload must be a CanonicalInterfacePayload value.",
            ValidationCategory.SCHEMA,
            field="canonical_payload",
            code="invalid_canonical_payload",
        )
    else:
        result.merge(validate_canonical_interface_payload(canonical_payload))

    return result
