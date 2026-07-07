from __future__ import annotations

from packages.runtime.validation import CANONICAL_RUNTIME_ARTIFACT_TYPES
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .contract import RuntimeRegistrationContract, validate_runtime_registration_contract
from .descriptor import RuntimeContextDescriptor, validate_runtime_context_descriptor
from .lookup import RuntimeRegistryEntry, validate_runtime_registry_entry


def validate_runtime_registry_artifact_composition(
    artifact: CanonicalObject,
    context_descriptor: RuntimeContextDescriptor,
    field_prefix: str = "registry_composition",
) -> ValidationResult:
    """Verify registry context descriptors align with published runtime artifacts."""

    result = ValidationResult()

    if artifact.object_type not in CANONICAL_RUNTIME_ARTIFACT_TYPES:
        result.add_error(
            "Artifact type is not an approved canonical Runtime Foundation artifact.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.artifact.object_type",
            code="invalid_registry_artifact_type",
        )
        return result

    if context_descriptor.artifact_object_type != artifact.object_type:
        result.add_error(
            "Context descriptor artifact type must match the supplied runtime artifact.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.context_descriptor.artifact_object_type",
            code="registry_artifact_type_mismatch",
        )

    result.merge(validate_runtime_context_descriptor(context_descriptor))

    return result


def compose_runtime_registry_entry(
    registration_contract: RuntimeRegistrationContract,
) -> RuntimeRegistryEntry:
    """Compose a deterministic registry entry from a canonical registration contract."""

    validation = validate_runtime_registration_contract(registration_contract)
    if not validation.is_valid:
        raise ValueError("Registration contract failed validation before composition.")

    entry = RuntimeRegistryEntry(
        registration_identifier=registration_contract.registration_identifier,
        registration_contract=registration_contract,
        context_descriptor=registration_contract.context_descriptor,
    )

    entry_validation = validate_runtime_registry_entry(entry)
    if not entry_validation.is_valid:
        raise ValueError("Registry entry failed validation after composition.")

    return entry
