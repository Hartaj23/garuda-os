from __future__ import annotations

from dataclasses import dataclass
from typing import Final
from uuid import UUID

from packages.interface import CanonicalInterfaceRequest, CanonicalInterfaceResponse
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .common import IntegrationContractMetadata, validate_integration_contract_metadata

ALLOWED_INTERFACE_CONTRACT_TYPES: Final[tuple[str, ...]] = (
    "CanonicalInterfaceRequest",
    "CanonicalInterfaceResponse",
)


@dataclass(frozen=True, slots=True)
class IntegrationContractSubordination:
    """Subordination metadata linking an integration contract to a canonical interface contract."""

    interface_contract_object_id: str
    interface_contract_object_type: str
    subordination_metadata: IntegrationContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.subordination_metadata is None:
            object.__setattr__(self, "subordination_metadata", IntegrationContractMetadata())

    def to_dict(self) -> dict[str, object]:
        subordination_metadata = self.subordination_metadata or IntegrationContractMetadata()
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


def validate_integration_contract_subordination(
    subordination: object,
    field_prefix: str = "interface_subordination",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(subordination, IntegrationContractSubordination):
        result.add_error(
            "Interface subordination must be an IntegrationContractSubordination value.",
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
            validate_integration_contract_metadata(
                subordination_metadata,
                field_prefix=f"{field_prefix}.subordination_metadata",
            )
        )

    return result


def build_interface_subordination(
    interface_contract: CanonicalInterfaceRequest | CanonicalInterfaceResponse,
    subordination_metadata: IntegrationContractMetadata | None = None,
) -> IntegrationContractSubordination:
    return IntegrationContractSubordination(
        interface_contract_object_id=str(interface_contract.object_id),
        interface_contract_object_type=interface_contract.object_type,
        subordination_metadata=subordination_metadata,
    )
