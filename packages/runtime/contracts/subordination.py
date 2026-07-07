from __future__ import annotations

from dataclasses import dataclass
from typing import Final
from uuid import UUID

from packages.integration import CanonicalIntegrationContract
from packages.interface import CanonicalInterfaceRequest, CanonicalInterfaceResponse
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import RuntimeContractMetadata, validate_runtime_contract_metadata

ALLOWED_INTEGRATION_CONTRACT_TYPES: Final[tuple[str, ...]] = ("CanonicalIntegrationContract",)
ALLOWED_INTERFACE_CONTRACT_TYPES: Final[tuple[str, ...]] = (
    "CanonicalInterfaceRequest",
    "CanonicalInterfaceResponse",
)


@dataclass(frozen=True, slots=True)
class RuntimeIntegrationContractSubordination:
    """Structural subordination metadata linking a runtime contract to an integration contract."""

    integration_contract_object_id: str
    integration_contract_object_type: str
    subordination_metadata: RuntimeContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.subordination_metadata is None:
            object.__setattr__(self, "subordination_metadata", RuntimeContractMetadata())

    def to_dict(self) -> dict[str, object]:
        subordination_metadata = self.subordination_metadata or RuntimeContractMetadata()
        return {
            "integration_contract_object_id": self.integration_contract_object_id,
            "integration_contract_object_type": self.integration_contract_object_type,
            "subordination_metadata": subordination_metadata.to_dict(),
        }

    def is_subordinate_to(self, integration_contract: CanonicalObject) -> bool:
        return (
            str(integration_contract.object_id) == self.integration_contract_object_id
            and integration_contract.object_type == self.integration_contract_object_type
            and self.integration_contract_object_type in ALLOWED_INTEGRATION_CONTRACT_TYPES
        )


@dataclass(frozen=True, slots=True)
class RuntimeInterfaceContractSubordination:
    """Structural subordination metadata linking a runtime contract to an interface contract."""

    interface_contract_object_id: str
    interface_contract_object_type: str
    subordination_metadata: RuntimeContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.subordination_metadata is None:
            object.__setattr__(self, "subordination_metadata", RuntimeContractMetadata())

    def to_dict(self) -> dict[str, object]:
        subordination_metadata = self.subordination_metadata or RuntimeContractMetadata()
        return {
            "interface_contract_object_id": self.interface_contract_object_id,
            "interface_contract_object_type": self.interface_contract_object_type,
            "subordination_metadata": subordination_metadata.to_dict(),
        }

    def is_subordinate_to(self, interface_contract: CanonicalObject) -> bool:
        return (
            str(interface_contract.object_id) == self.interface_contract_object_id
            and interface_contract.object_type == self.interface_contract_object_type
            and self.interface_contract_object_type in ALLOWED_INTERFACE_CONTRACT_TYPES
        )


def validate_runtime_integration_contract_subordination(
    subordination: object,
    field_prefix: str = "integration_subordination",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(subordination, RuntimeIntegrationContractSubordination):
        result.add_error(
            "Integration subordination must be a RuntimeIntegrationContractSubordination value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_integration_subordination",
        )
        return result

    if (
        not isinstance(subordination.integration_contract_object_id, str)
        or not subordination.integration_contract_object_id
    ):
        result.add_error(
            "Integration contract object identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.integration_contract_object_id",
            code="invalid_integration_contract_object_id",
        )
    else:
        try:
            UUID(subordination.integration_contract_object_id)
        except ValueError:
            result.add_error(
                "Integration contract object identifier must be a UUID string.",
                ValidationCategory.IDENTITY,
                field=f"{field_prefix}.integration_contract_object_id",
                code="invalid_integration_contract_object_id_format",
            )

    if (
        not isinstance(subordination.integration_contract_object_type, str)
        or subordination.integration_contract_object_type not in ALLOWED_INTEGRATION_CONTRACT_TYPES
    ):
        result.add_error(
            "Integration contract object type must be a canonical integration contract type.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.integration_contract_object_type",
            code="invalid_integration_contract_object_type",
        )

    subordination_metadata = subordination.subordination_metadata
    if subordination_metadata is not None:
        result.merge(
            validate_runtime_contract_metadata(
                subordination_metadata,
                field_prefix=f"{field_prefix}.subordination_metadata",
            )
        )

    return result


def validate_runtime_interface_contract_subordination(
    subordination: object,
    field_prefix: str = "interface_subordination",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(subordination, RuntimeInterfaceContractSubordination):
        result.add_error(
            "Interface subordination must be a RuntimeInterfaceContractSubordination value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_interface_subordination",
        )
        return result

    if (
        not isinstance(subordination.interface_contract_object_id, str)
        or not subordination.interface_contract_object_id
    ):
        result.add_error(
            "Interface contract object identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.interface_contract_object_id",
            code="invalid_interface_contract_object_id",
        )
    else:
        try:
            UUID(subordination.interface_contract_object_id)
        except ValueError:
            result.add_error(
                "Interface contract object identifier must be a UUID string.",
                ValidationCategory.IDENTITY,
                field=f"{field_prefix}.interface_contract_object_id",
                code="invalid_interface_contract_object_id_format",
            )

    if (
        not isinstance(subordination.interface_contract_object_type, str)
        or subordination.interface_contract_object_type not in ALLOWED_INTERFACE_CONTRACT_TYPES
    ):
        result.add_error(
            "Interface contract object type must be a canonical interface contract type.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.interface_contract_object_type",
            code="invalid_interface_contract_object_type",
        )

    subordination_metadata = subordination.subordination_metadata
    if subordination_metadata is not None:
        result.merge(
            validate_runtime_contract_metadata(
                subordination_metadata,
                field_prefix=f"{field_prefix}.subordination_metadata",
            )
        )

    return result


def build_integration_subordination(
    integration_contract: CanonicalIntegrationContract,
    subordination_metadata: RuntimeContractMetadata | None = None,
) -> RuntimeIntegrationContractSubordination:
    return RuntimeIntegrationContractSubordination(
        integration_contract_object_id=str(integration_contract.object_id),
        integration_contract_object_type=integration_contract.object_type,
        subordination_metadata=subordination_metadata,
    )


def build_interface_subordination(
    interface_contract: CanonicalInterfaceRequest | CanonicalInterfaceResponse,
    subordination_metadata: RuntimeContractMetadata | None = None,
) -> RuntimeInterfaceContractSubordination:
    return RuntimeInterfaceContractSubordination(
        interface_contract_object_id=str(interface_contract.object_id),
        interface_contract_object_type=interface_contract.object_type,
        subordination_metadata=subordination_metadata,
    )
