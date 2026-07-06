from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .contract import InterfaceRegistrationContract, validate_interface_registration_contract
from .descriptor import InterfaceAdapterDescriptor


@dataclass(frozen=True, slots=True)
class InterfaceRegistryEntry:
    registration_identifier: str
    registration_contract: InterfaceRegistrationContract
    adapter_descriptor: InterfaceAdapterDescriptor

    def __post_init__(self) -> None:
        if self.registration_identifier != self.registration_contract.registration_identifier:
            raise ValueError(
                "registration_identifier must match registration_contract.registration_identifier"
            )
        if self.adapter_descriptor != self.registration_contract.adapter_descriptor:
            raise ValueError("adapter_descriptor must match registration_contract.adapter_descriptor")

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "registration_contract": self.registration_contract.to_dict(),
            "adapter_descriptor": self.adapter_descriptor.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceRegistryLookupCriteria:
    registration_identifier: str | None = None
    artifact_object_type: str | None = None
    adapter_identifier: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "artifact_object_type": self.artifact_object_type,
            "adapter_identifier": self.adapter_identifier,
        }


@dataclass(frozen=True, slots=True)
class InterfaceRegistryLookupResult:
    entries: tuple[InterfaceRegistryEntry, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))

    def to_dict(self) -> dict[str, object]:
        return {
            "entries": [entry.to_dict() for entry in self.entries],
        }


def validate_interface_registry_entry(
    entry: object,
    field_prefix: str = "registry_entry",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(entry, InterfaceRegistryEntry):
        result.add_error(
            "Registry entry must be an InterfaceRegistryEntry value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_registry_entry",
        )
        return result

    if not isinstance(entry.registration_identifier, str) or not entry.registration_identifier:
        result.add_error(
            "Registration identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.registration_identifier",
            code="invalid_registration_identifier",
        )

    if not isinstance(entry.registration_contract, InterfaceRegistrationContract):
        result.add_error(
            "Registration contract must be an InterfaceRegistrationContract value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.registration_contract",
            code="invalid_registration_contract",
        )
    else:
        result.merge(validate_interface_registration_contract(entry.registration_contract))

    if not isinstance(entry.adapter_descriptor, InterfaceAdapterDescriptor):
        result.add_error(
            "Adapter descriptor must be an InterfaceAdapterDescriptor value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.adapter_descriptor",
            code="invalid_adapter_descriptor",
        )

    return result
