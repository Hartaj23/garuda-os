from __future__ import annotations

from typing import Any

from packages.runtime.contracts import (
    CanonicalRuntimeContract,
    validate_runtime_integration_contract_subordination,
    validate_runtime_interface_contract_subordination,
)
from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .composition import compose_runtime_validation_results
from .descriptor import (
    RuntimeValidationDescriptor,
    TARGET_OBJECT_TYPES,
    validate_runtime_validation_descriptor,
)
from .metadata import RuntimeValidationMetadata, validate_runtime_validation_metadata
from .policy import (
    RuntimeSubordinationRule,
    RuntimeValidationPolicy,
    validate_artifact_version_compatibility,
    validate_runtime_validation_policy,
)
from .result import RuntimeValidationOutcome


CANONICAL_RUNTIME_ARTIFACT_TYPES = frozenset(TARGET_OBJECT_TYPES.values())

FORBIDDEN_VARIABILITY_OBJECT_PREFIXES = (
    "CanonicalMemory",
    "CanonicalKnowledge",
    "CanonicalContext",
    "CanonicalReasoning",
    "CanonicalDecision",
    "CanonicalAction",
    "CanonicalExecution",
    "UniversalExecution",
)

FORBIDDEN_OPERATIONAL_OBJECT_PREFIXES = (
    "UniversalExecution",
    "ExecutionWorkspace",
    "ExecutionChain",
    "ExecutionStrategy",
)


def validate_runtime_variability_containment(
    artifact: CanonicalObject,
    field_prefix: str = "artifact",
) -> ValidationResult:
    """Verify runtime variability terminates at the Runtime Foundation boundary."""

    result = ValidationResult()

    if artifact.object_type not in CANONICAL_RUNTIME_ARTIFACT_TYPES:
        result.add_error(
            "Artifact type is not an approved canonical Runtime Foundation artifact.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.object_type",
            code="variability_containment_violation",
        )
        return result

    for forbidden_prefix in FORBIDDEN_VARIABILITY_OBJECT_PREFIXES:
        if artifact.object_type.startswith(forbidden_prefix):
            result.add_error(
                "Runtime artifacts must not inherit cognitive or execution foundation variability.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.object_type",
                code="variability_containment_violation",
            )
            break

    return result


def validate_runtime_operational_runtime_exclusion(
    artifact: CanonicalObject,
    field_prefix: str = "artifact",
) -> ValidationResult:
    """Verify runtime validation artifacts exclude Operational Runtime semantics."""

    result = ValidationResult()

    if artifact.object_type == "UniversalExecution":
        result.add_error(
            "Runtime validation must not evaluate Universal Execution Foundation artifacts.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.object_type",
            code="operational_runtime_exclusion_violation",
        )
        return result

    for forbidden_prefix in FORBIDDEN_OPERATIONAL_OBJECT_PREFIXES:
        if artifact.object_type.startswith(forbidden_prefix):
            result.add_error(
                "Runtime validation must not evaluate Operational Runtime artifact types.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.object_type",
                code="operational_runtime_exclusion_violation",
            )
            break

    return result


def validate_runtime_subordination_requirement(
    artifact: CanonicalObject,
    subordination_rule: RuntimeSubordinationRule,
    *,
    integration_contract: CanonicalObject | None = None,
    interface_contract: CanonicalObject | None = None,
    field_prefix: str = "artifact",
) -> ValidationResult:
    result = ValidationResult()

    if not subordination_rule.require_valid_subordination:
        return result

    if not isinstance(artifact, CanonicalRuntimeContract):
        return result

    integration_subordination = artifact.integration_subordination
    interface_subordination = artifact.interface_subordination
    result.merge(validate_runtime_integration_contract_subordination(integration_subordination))
    result.merge(validate_runtime_interface_contract_subordination(interface_subordination))

    if subordination_rule.require_integration_contract_match:
        if integration_contract is None:
            result.add_error(
                "Integration contract reference is required for subordination match validation.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.integration_subordination",
                code="missing_integration_contract_reference",
            )
        elif not integration_subordination.is_subordinate_to(integration_contract):
            result.add_error(
                "Runtime contract integration subordination does not match supplied integration contract.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.integration_subordination",
                code="integration_subordination_mismatch",
            )

    if subordination_rule.require_interface_contract_match:
        if interface_contract is None:
            result.add_error(
                "Interface contract reference is required for subordination match validation.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.interface_subordination",
                code="missing_interface_contract_reference",
            )
        elif not interface_subordination.is_subordinate_to(interface_contract):
            result.add_error(
                "Runtime contract interface subordination does not match supplied interface contract.",
                ValidationCategory.SCHEMA,
                field=f"{field_prefix}.interface_subordination",
                code="interface_subordination_mismatch",
            )

    return result


def evaluate_runtime_artifact(
    artifact: object,
    policy: RuntimeValidationPolicy,
    *,
    integration_contract: CanonicalObject | None = None,
    interface_contract: CanonicalObject | None = None,
) -> ValidationResult:
    """Pure deterministic evaluation of a canonical runtime artifact.

    Validation Containment Invariant:
    Only canonical Runtime Foundation artifacts may enter the Validation Framework.

    evaluate_runtime_artifact derives its result solely from the supplied canonical
    artifact, validation policy, and optional contract references. It has no side
    effects, hidden state, environmental dependencies, or external lookups.
    """
    if not isinstance(artifact, CanonicalObject):
        result = ValidationResult()
        result.add_error(
            "Validation requires a canonical Runtime Foundation artifact.",
            ValidationCategory.SCHEMA,
            field="artifact",
            code="invalid_validation_artifact",
        )
        return result

    if artifact.object_type not in CANONICAL_RUNTIME_ARTIFACT_TYPES:
        result = ValidationResult()
        result.add_error(
            "Artifact type is not an approved canonical Runtime Foundation artifact.",
            ValidationCategory.SCHEMA,
            field="artifact.object_type",
            code="invalid_validation_artifact_type",
        )
        return result

    policy_result = validate_runtime_validation_policy(policy)
    if policy.target_object_type != artifact.object_type:
        policy_result.add_error(
            "Validation policy target does not match artifact object type.",
            ValidationCategory.SCHEMA,
            field="artifact.object_type",
            code="policy_target_mismatch",
        )

    variability_result = validate_runtime_variability_containment(artifact)
    operational_result = validate_runtime_operational_runtime_exclusion(artifact)

    version_rule = policy.version_rule
    version_result = ValidationResult()
    if version_rule is not None:
        version_result = validate_artifact_version_compatibility(artifact, version_rule)

    subordination_rule = policy.subordination_rule or RuntimeSubordinationRule()
    subordination_result = validate_runtime_subordination_requirement(
        artifact,
        subordination_rule,
        integration_contract=integration_contract,
        interface_contract=interface_contract,
    )

    artifact_result = artifact.validate()

    return compose_runtime_validation_results(
        policy_result,
        variability_result,
        operational_result,
        version_result,
        subordination_result,
        artifact_result,
    )


def compose_cross_model_runtime_validation(
    artifact: CanonicalObject,
    *policies: RuntimeValidationPolicy,
    integration_contract: CanonicalObject | None = None,
    interface_contract: CanonicalObject | None = None,
) -> ValidationResult:
    """Compose deterministic validation across multiple runtime validation policies."""

    if not policies:
        result = ValidationResult()
        result.add_error(
            "At least one validation policy is required for cross-model composition.",
            ValidationCategory.SCHEMA,
            field="policies",
            code="missing_validation_policies",
        )
        return result

    evaluations = [
        evaluate_runtime_artifact(
            artifact,
            policy,
            integration_contract=integration_contract,
            interface_contract=interface_contract,
        )
        for policy in policies
    ]
    return compose_runtime_validation_results(*evaluations)


class RuntimeValidationRecord(CanonicalObject):
    """Record of a canonical runtime validation evaluation.

    Contract invariants:
    - Required fields: validation_descriptor, validation_policy, validation_outcome
    - Optional fields: validation_metadata, Platform Core constructor fields
    - Immutable after construction: all validation-specific fields
    - Equality semantics: not overridden; object identity semantics apply
    - Identity semantics: Platform Core object_id and object_type inherited unchanged
    - Serialization: inherited Platform Core fields via ObjectSerializer; full record via to_dict()
    """

    def __init__(
        self,
        validation_descriptor: RuntimeValidationDescriptor,
        validation_policy: RuntimeValidationPolicy,
        validation_outcome: RuntimeValidationOutcome,
        validation_metadata: RuntimeValidationMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._validation_descriptor = validation_descriptor
        self._validation_policy = validation_policy
        self._validation_outcome = validation_outcome
        self._validation_metadata = validation_metadata or RuntimeValidationMetadata()
        self.register_validation_hook(validate_runtime_validation_record)

    @property
    def validation_descriptor(self) -> RuntimeValidationDescriptor:
        return self._validation_descriptor

    @property
    def validation_policy(self) -> RuntimeValidationPolicy:
        return self._validation_policy

    @property
    def validation_outcome(self) -> RuntimeValidationOutcome:
        return self._validation_outcome

    @property
    def validation_metadata(self) -> RuntimeValidationMetadata:
        return self._validation_metadata

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
            "validation_descriptor": self.validation_descriptor.to_dict(),
            "validation_policy": self.validation_policy.to_dict(),
            "validation_outcome": self.validation_outcome.to_dict(),
            "validation_metadata": self.validation_metadata.to_dict(),
        }


def validate_runtime_validation_record(obj: RuntimeValidationRecord) -> ValidationResult:
    result = ValidationResult()

    validation_descriptor = getattr(obj, "validation_descriptor", None)
    if not isinstance(validation_descriptor, RuntimeValidationDescriptor):
        result.add_error(
            "Validation descriptor must be a RuntimeValidationDescriptor value.",
            ValidationCategory.SCHEMA,
            field="validation_descriptor",
            code="invalid_validation_descriptor",
        )
    else:
        result.merge(validate_runtime_validation_descriptor(validation_descriptor))

    validation_policy = getattr(obj, "validation_policy", None)
    if not isinstance(validation_policy, RuntimeValidationPolicy):
        result.add_error(
            "Validation policy must be a RuntimeValidationPolicy value.",
            ValidationCategory.SCHEMA,
            field="validation_policy",
            code="invalid_validation_policy",
        )
    else:
        result.merge(validate_runtime_validation_policy(validation_policy))

    validation_outcome = getattr(obj, "validation_outcome", None)
    if not isinstance(validation_outcome, RuntimeValidationOutcome):
        result.add_error(
            "Validation outcome must be a RuntimeValidationOutcome value.",
            ValidationCategory.SCHEMA,
            field="validation_outcome",
            code="invalid_validation_outcome",
        )

    validation_metadata = getattr(obj, "validation_metadata", None)
    if not isinstance(validation_metadata, RuntimeValidationMetadata):
        result.add_error(
            "Validation metadata must be a RuntimeValidationMetadata value.",
            ValidationCategory.METADATA,
            field="validation_metadata",
            code="invalid_validation_metadata",
        )
    else:
        result.merge(validate_runtime_validation_metadata(validation_metadata))

    return result


__all__ = [
    "CANONICAL_RUNTIME_ARTIFACT_TYPES",
    "FORBIDDEN_OPERATIONAL_OBJECT_PREFIXES",
    "FORBIDDEN_VARIABILITY_OBJECT_PREFIXES",
    "RuntimeValidationRecord",
    "compose_cross_model_runtime_validation",
    "evaluate_runtime_artifact",
    "validate_runtime_operational_runtime_exclusion",
    "validate_runtime_subordination_requirement",
    "validate_runtime_validation_record",
    "validate_runtime_variability_containment",
]
