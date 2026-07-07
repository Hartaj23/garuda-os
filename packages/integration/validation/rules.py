from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.objects import ValidationCategory, ValidationResult

from .metadata import IntegrationValidationMetadata, validate_integration_validation_metadata


class IntegrationValidationRuleKind(StrEnum):
    ARTIFACT_STRUCTURE = "artifact_structure"
    VERSION_COMPATIBILITY = "version_compatibility"
    SUBORDINATION = "subordination"
    VARIABILITY_CONTAINMENT = "variability_containment"


@dataclass(frozen=True, slots=True)
class IntegrationValidationRule:
    """Descriptive validation rule model for integration artifact evaluation."""

    rule_identifier: str
    rule_kind: IntegrationValidationRuleKind
    rule_metadata: IntegrationValidationMetadata | None = None

    def __post_init__(self) -> None:
        if self.rule_metadata is None:
            object.__setattr__(self, "rule_metadata", IntegrationValidationMetadata())

    def to_dict(self) -> dict[str, object]:
        rule_metadata = self.rule_metadata or IntegrationValidationMetadata()
        return {
            "rule_identifier": self.rule_identifier,
            "rule_kind": self.rule_kind.value,
            "rule_metadata": rule_metadata.to_dict(),
        }


def validate_integration_validation_rule(
    rule: object,
    field_prefix: str = "validation_rule",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(rule, IntegrationValidationRule):
        result.add_error(
            "Validation rule must be an IntegrationValidationRule value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_validation_rule",
        )
        return result

    if not isinstance(rule.rule_identifier, str) or not rule.rule_identifier:
        result.add_error(
            "Rule identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.rule_identifier",
            code="invalid_rule_identifier",
        )

    if not isinstance(rule.rule_kind, IntegrationValidationRuleKind):
        result.add_error(
            "Rule kind must be an IntegrationValidationRuleKind value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.rule_kind",
            code="invalid_rule_kind",
        )

    rule_metadata = rule.rule_metadata
    if rule_metadata is not None:
        result.merge(
            validate_integration_validation_metadata(
                rule_metadata,
                field_prefix=f"{field_prefix}.rule_metadata",
            )
        )

    return result
