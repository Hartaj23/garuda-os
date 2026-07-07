from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .contract import RuntimeRegistrationContract, validate_runtime_registration_contract
from .descriptor import RuntimeContextDescriptor


@dataclass(frozen=True, slots=True)
class RuntimeRegistryEntry:
    registration_identifier: str
    registration_contract: RuntimeRegistrationContract
    context_descriptor: RuntimeContextDescriptor

    def __post_init__(self) -> None:
        if self.registration_identifier != self.registration_contract.registration_identifier:
            raise ValueError(
                "registration_identifier must match registration_contract.registration_identifier"
            )
        if self.context_descriptor != self.registration_contract.context_descriptor:
            raise ValueError(
                "context_descriptor must match registration_contract.context_descriptor"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "registration_contract": self.registration_contract.to_dict(),
            "context_descriptor": self.context_descriptor.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class RuntimeRegistryLookupCriteria:
    registration_identifier: str | None = None
    artifact_object_type: str | None = None
    context_identifier: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "registration_identifier": self.registration_identifier,
            "artifact_object_type": self.artifact_object_type,
            "context_identifier": self.context_identifier,
        }


@dataclass(frozen=True, slots=True)
class RuntimeRegistryLookupResult:
    entries: tuple[RuntimeRegistryEntry, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))

    def to_dict(self) -> dict[str, object]:
        return {
            "entries": [entry.to_dict() for entry in self.entries],
        }


def validate_runtime_registry_entry(
    entry: object,
    field_prefix: str = "registry_entry",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(entry, RuntimeRegistryEntry):
        result.add_error(
            "Registry entry must be a RuntimeRegistryEntry value.",
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

    if not isinstance(entry.registration_contract, RuntimeRegistrationContract):
        result.add_error(
            "Registration contract must be a RuntimeRegistrationContract value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.registration_contract",
            code="invalid_registration_contract",
        )
    else:
        result.merge(validate_runtime_registration_contract(entry.registration_contract))

    if not isinstance(entry.context_descriptor, RuntimeContextDescriptor):
        result.add_error(
            "Context descriptor must be a RuntimeContextDescriptor value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.context_descriptor",
            code="invalid_context_descriptor",
        )

    return result
