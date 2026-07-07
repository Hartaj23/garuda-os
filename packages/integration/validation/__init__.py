from .composition import compose_integration_validation_results
from .descriptor import (
    IntegrationValidationDescriptor,
    IntegrationValidationTarget,
    TARGET_OBJECT_TYPES,
    validate_integration_validation_descriptor,
)
from .errors import (
    IntegrationValidationIssue,
    IntegrationValidationIssueCollection,
    validate_integration_validation_issue,
)
from .framework import (
    CANONICAL_INTEGRATION_ARTIFACT_TYPES,
    IntegrationValidationRecord,
    compose_cross_model_integration_validation,
    evaluate_integration_artifact,
    validate_integration_subordination_requirement,
    validate_integration_validation_record,
    validate_integration_variability_containment,
)
from .metadata import IntegrationValidationMetadata, validate_integration_validation_metadata
from .policy import (
    IntegrationSubordinationRule,
    IntegrationValidationPolicy,
    IntegrationVersionCompatibilityRule,
    validate_artifact_version_compatibility,
    validate_integration_subordination_rule,
    validate_integration_validation_policy,
    validate_integration_version_compatibility_rule,
)
from .report import (
    IntegrationValidationReport,
    build_integration_validation_report,
    validate_integration_validation_report,
)
from .result import (
    IntegrationValidationOutcome,
    serialize_integration_validation_outcome,
    validation_result_to_outcome,
)
from .rules import (
    IntegrationValidationRule,
    IntegrationValidationRuleKind,
    validate_integration_validation_rule,
)

__all__ = [
    "CANONICAL_INTEGRATION_ARTIFACT_TYPES",
    "IntegrationSubordinationRule",
    "IntegrationValidationDescriptor",
    "IntegrationValidationIssue",
    "IntegrationValidationIssueCollection",
    "IntegrationValidationMetadata",
    "IntegrationValidationOutcome",
    "IntegrationValidationPolicy",
    "IntegrationValidationRecord",
    "IntegrationValidationReport",
    "IntegrationValidationRule",
    "IntegrationValidationRuleKind",
    "IntegrationValidationTarget",
    "IntegrationVersionCompatibilityRule",
    "TARGET_OBJECT_TYPES",
    "build_integration_validation_report",
    "compose_cross_model_integration_validation",
    "compose_integration_validation_results",
    "evaluate_integration_artifact",
    "serialize_integration_validation_outcome",
    "validate_artifact_version_compatibility",
    "validate_integration_subordination_requirement",
    "validate_integration_subordination_rule",
    "validate_integration_validation_descriptor",
    "validate_integration_validation_issue",
    "validate_integration_validation_metadata",
    "validate_integration_validation_policy",
    "validate_integration_validation_record",
    "validate_integration_validation_report",
    "validate_integration_validation_rule",
    "validate_integration_variability_containment",
    "validate_integration_version_compatibility_rule",
    "validation_result_to_outcome",
]
