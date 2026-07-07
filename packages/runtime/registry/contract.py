from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .descriptor import RuntimeContextDescriptor, validate_runtime_context_descriptor
from .metadata import RuntimeRegistryMetadata, validate_runtime_registry_metadata


class RuntimeRegistrationContract(CanonicalObject):
    """Canonical registration contract for Runtime Registry catalog entries.

    Registry Containment Invariant:
    The Runtime Registry terminates registry knowledge within the Runtime Foundation.
    Registry contents do not expose external technology representations, provider implementations,
    execution engine bindings, or internal cognitive implementation details.

    Contract invariants:
    - Required fields: registration_identifier, context_descriptor, registration_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all registration-specific fields
    - Identity semantics: registration_identifier is the stable canonical catalog identity
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        registration_identifier: str,
        context_descriptor: RuntimeContextDescriptor,
        registration_metadata: RuntimeRegistryMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._registration_identifier = registration_identifier
        self._context_descriptor = context_descriptor
        self._registration_metadata = registration_metadata or RuntimeRegistryMetadata()
        self.register_validation_hook(validate_runtime_registration_contract)

    @property
    def registration_identifier(self) -> str:
        return self._registration_identifier

    @property
    def context_descriptor(self) -> RuntimeContextDescriptor:
        return self._context_descriptor

    @property
    def registration_metadata(self) -> RuntimeRegistryMetadata:
        return self._registration_metadata

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
            "registration_identifier": self.registration_identifier,
            "context_descriptor": self.context_descriptor.to_dict(),
            "registration_metadata": self.registration_metadata.to_dict(),
        }


def validate_runtime_registration_contract(
    obj: RuntimeRegistrationContract,
) -> ValidationResult:
    result = ValidationResult()

    if (
        not isinstance(getattr(obj, "registration_identifier", None), str)
        or not obj.registration_identifier
    ):
        result.add_error(
            "Registration identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field="registration_identifier",
            code="invalid_registration_identifier",
        )

    context_descriptor = getattr(obj, "context_descriptor", None)
    if not isinstance(context_descriptor, RuntimeContextDescriptor):
        result.add_error(
            "Context descriptor must be a RuntimeContextDescriptor value.",
            ValidationCategory.SCHEMA,
            field="context_descriptor",
            code="invalid_context_descriptor",
        )
    else:
        result.merge(validate_runtime_context_descriptor(context_descriptor))

    registration_metadata = getattr(obj, "registration_metadata", None)
    if not isinstance(registration_metadata, RuntimeRegistryMetadata):
        result.add_error(
            "Registration metadata must be a RuntimeRegistryMetadata value.",
            ValidationCategory.METADATA,
            field="registration_metadata",
            code="invalid_registration_metadata",
        )
    else:
        result.merge(validate_runtime_registry_metadata(registration_metadata))

    return result
