from __future__ import annotations

from dataclasses import dataclass

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .descriptor import IntegrationValidationTarget, validate_integration_validation_descriptor
from .metadata import IntegrationValidationMetadata, validate_integration_validation_metadata
from .rules import IntegrationValidationRule, validate_integration_validation_rule


@dataclass(frozen=True, slots=True)
class IntegrationVersionCompatibilityRule:
    required_schema_version: str = "1.0"
    minimum_object_version: int = 1

    def to_dict(self) -> dict[str, object]:
        return {
            "required_schema_version": self.required_schema_version,
            "minimum_object_version": self.minimum_object_version,
        }


@dataclass(frozen=True, slots=True)
class IntegrationSubordinationRule:
    """Subordination requirements for integration contract validation."""

    require_valid_subordination: bool = True
    require_interface_contract_match: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "require_valid_subordination": self.require_valid_subordination,
            "require_interface_contract_match": self.require_interface_contract_match,
        }


@dataclass(frozen=True, slots=True)
class IntegrationValidationPolicy:
    """Immutable validation policy identified by policy_identifier and version rule."""

    policy_identifier: str
    validation_target: IntegrationValidationTarget
    target_object_type: str
    version_rule: IntegrationVersionCompatibilityRule | None = None
    subordination_rule: IntegrationSubordinationRule | None = None
    validation_rules: tuple[IntegrationValidationRule, ...] = ()
    policy_metadata: IntegrationValidationMetadata | None = None
    policy_version: str = "1.0"

    def __post_init__(self) -> None:
        if self.version_rule is None:
            object.__setattr__(self, "version_rule", IntegrationVersionCompatibilityRule())
        if self.subordination_rule is None:
            object.__setattr__(self, "subordination_rule", IntegrationSubordinationRule())
        if self.policy_metadata is None:
            object.__setattr__(self, "policy_metadata", IntegrationValidationMetadata())
        object.__setattr__(self, "validation_rules", tuple(self.validation_rules))

    def to_dict(self) -> dict[str, object]:
        version_rule = self.version_rule or IntegrationVersionCompatibilityRule()
        subordination_rule = self.subordination_rule or IntegrationSubordinationRule()
        policy_metadata = self.policy_metadata or IntegrationValidationMetadata()
        return {
            "policy_identifier": self.policy_identifier,
            "policy_version": self.policy_version,
            "validation_target": self.validation_target.value,
            "target_object_type": self.target_object_type,
            "version_rule": version_rule.to_dict(),
            "subordination_rule": subordination_rule.to_dict(),
            "validation_rules": [rule.to_dict() for rule in self.validation_rules],
            "policy_metadata": policy_metadata.to_dict(),
        }


def validate_integration_version_compatibility_rule(
    rule: object,
    field_prefix: str = "version_rule",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(rule, IntegrationVersionCompatibilityRule):
        result.add_error(
            "Version compatibility rule must be an IntegrationVersionCompatibilityRule value.",
            ValidationCategory.VERSION,
            field=field_prefix,
            code="invalid_version_compatibility_rule",
        )
        return result

    if not isinstance(rule.required_schema_version, str) or not rule.required_schema_version:
        result.add_error(
            "Required schema version must be a non-empty string.",
            ValidationCategory.VERSION,
            field=f"{field_prefix}.required_schema_version",
            code="invalid_required_schema_version",
        )

    if not isinstance(rule.minimum_object_version, int) or rule.minimum_object_version < 1:
        result.add_error(
            "Minimum object version must be an integer greater than or equal to 1.",
            ValidationCategory.VERSION,
            field=f"{field_prefix}.minimum_object_version",
            code="invalid_minimum_object_version",
        )

    return result


def validate_integration_subordination_rule(
    rule: object,
    field_prefix: str = "subordination_rule",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(rule, IntegrationSubordinationRule):
        result.add_error(
            "Subordination rule must be an IntegrationSubordinationRule value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_subordination_rule",
        )

    return result


def validate_integration_validation_policy(
    policy: object,
    field_prefix: str = "validation_policy",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(policy, IntegrationValidationPolicy):
        result.add_error(
            "Validation policy must be an IntegrationValidationPolicy value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_validation_policy",
        )
        return result

    if not isinstance(policy.policy_identifier, str) or not policy.policy_identifier:
        result.add_error(
            "Policy identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.policy_identifier",
            code="invalid_policy_identifier",
        )

    if not isinstance(policy.policy_version, str) or not policy.policy_version:
        result.add_error(
            "Policy version must be a non-empty string.",
            ValidationCategory.VERSION,
            field=f"{field_prefix}.policy_version",
            code="invalid_policy_version",
        )

    if not isinstance(policy.validation_target, IntegrationValidationTarget):
        result.add_error(
            "Validation target must be an IntegrationValidationTarget value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.validation_target",
            code="invalid_validation_target",
        )

    if not isinstance(policy.target_object_type, str) or not policy.target_object_type:
        result.add_error(
            "Target object type must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.target_object_type",
            code="invalid_target_object_type",
        )

    version_rule = policy.version_rule
    if version_rule is not None:
        result.merge(
            validate_integration_version_compatibility_rule(
                version_rule,
                field_prefix=f"{field_prefix}.version_rule",
            )
        )

    subordination_rule = policy.subordination_rule
    if subordination_rule is not None:
        result.merge(
            validate_integration_subordination_rule(
                subordination_rule,
                field_prefix=f"{field_prefix}.subordination_rule",
            )
        )

    for index, rule in enumerate(policy.validation_rules):
        result.merge(
            validate_integration_validation_rule(
                rule,
                field_prefix=f"{field_prefix}.validation_rules[{index}]",
            )
        )

    policy_metadata = policy.policy_metadata
    if policy_metadata is not None:
        result.merge(
            validate_integration_validation_metadata(
                policy_metadata,
                field_prefix=f"{field_prefix}.policy_metadata",
            )
        )

    return result


def validate_artifact_version_compatibility(
    artifact: CanonicalObject,
    rule: IntegrationVersionCompatibilityRule,
    field_prefix: str = "artifact",
) -> ValidationResult:
    result = ValidationResult()

    if artifact.schema_version != rule.required_schema_version:
        result.add_error(
            "Artifact schema version is incompatible with validation policy.",
            ValidationCategory.VERSION,
            field=f"{field_prefix}.schema_version",
            code="incompatible_schema_version",
        )

    if artifact.object_version < rule.minimum_object_version:
        result.add_error(
            "Artifact object version is below policy minimum.",
            ValidationCategory.VERSION,
            field=f"{field_prefix}.object_version",
            code="incompatible_object_version",
        )

    return result
