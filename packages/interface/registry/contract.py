from __future__ import annotations

from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .descriptor import InterfaceAdapterDescriptor, validate_interface_adapter_descriptor
from .metadata import InterfaceRegistryMetadata, validate_interface_registry_metadata


class InterfaceRegistrationContract(CanonicalObject):
    """Canonical registration contract for Interface Registry catalog entries.

    Registry Containment Invariant:
    The Interface Registry terminates registry knowledge within the Interface Foundation.
    Registry contents do not expose external technology representations or internal
    cognitive implementation details.

    Contract invariants:
    - Required fields: registration_identifier, adapter_descriptor, registration_metadata
    - Optional fields: Platform Core constructor fields
    - Immutable after construction: all registration-specific fields
    - Identity semantics: registration_identifier is the stable canonical catalog identity
    """

    def __init__(
        self,
        registration_identifier: str,
        adapter_descriptor: InterfaceAdapterDescriptor,
        registration_metadata: InterfaceRegistryMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._registration_identifier = registration_identifier
        self._adapter_descriptor = adapter_descriptor
        self._registration_metadata = registration_metadata or InterfaceRegistryMetadata()
        self.register_validation_hook(validate_interface_registration_contract)

    @property
    def registration_identifier(self) -> str:
        return self._registration_identifier

    @property
    def adapter_descriptor(self) -> InterfaceAdapterDescriptor:
        return self._adapter_descriptor

    @property
    def registration_metadata(self) -> InterfaceRegistryMetadata:
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
            "adapter_descriptor": self.adapter_descriptor.to_dict(),
            "registration_metadata": self.registration_metadata.to_dict(),
        }


def validate_interface_registration_contract(
    obj: InterfaceRegistrationContract,
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

    adapter_descriptor = getattr(obj, "adapter_descriptor", None)
    if not isinstance(adapter_descriptor, InterfaceAdapterDescriptor):
        result.add_error(
            "Adapter descriptor must be an InterfaceAdapterDescriptor value.",
            ValidationCategory.SCHEMA,
            field="adapter_descriptor",
            code="invalid_adapter_descriptor",
        )
    else:
        result.merge(validate_interface_adapter_descriptor(adapter_descriptor))

    registration_metadata = getattr(obj, "registration_metadata", None)
    if not isinstance(registration_metadata, InterfaceRegistryMetadata):
        result.add_error(
            "Registration metadata must be an InterfaceRegistryMetadata value.",
            ValidationCategory.METADATA,
            field="registration_metadata",
            code="invalid_registration_metadata",
        )
    else:
        result.merge(validate_interface_registry_metadata(registration_metadata))

    return result
