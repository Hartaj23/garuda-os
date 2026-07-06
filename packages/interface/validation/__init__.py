from .composition import compose_interface_validation_results
from .descriptor import (
    InterfaceValidationDescriptor,
    InterfaceValidationTarget,
    TARGET_OBJECT_TYPES,
    validate_interface_validation_descriptor,
)
from .errors import (
    InterfaceValidationIssue,
    InterfaceValidationIssueCollection,
    validate_interface_validation_issue,
)
from .framework import (
    CANONICAL_INTERFACE_ARTIFACT_TYPES,
    InterfaceValidationRecord,
    evaluate_interface_artifact,
    validate_interface_validation_record,
)
from .metadata import InterfaceValidationMetadata, validate_interface_validation_metadata
from .policy import (
    InterfaceValidationPolicy,
    InterfaceVersionCompatibilityRule,
    validate_artifact_version_compatibility,
    validate_interface_validation_policy,
    validate_interface_version_compatibility_rule,
)
from .result import InterfaceValidationOutcome, validation_result_to_outcome

__all__ = [
    "CANONICAL_INTERFACE_ARTIFACT_TYPES",
    "InterfaceValidationDescriptor",
    "InterfaceValidationIssue",
    "InterfaceValidationIssueCollection",
    "InterfaceValidationMetadata",
    "InterfaceValidationOutcome",
    "InterfaceValidationPolicy",
    "InterfaceValidationRecord",
    "InterfaceValidationTarget",
    "InterfaceVersionCompatibilityRule",
    "TARGET_OBJECT_TYPES",
    "compose_interface_validation_results",
    "evaluate_interface_artifact",
    "validate_artifact_version_compatibility",
    "validate_interface_validation_descriptor",
    "validate_interface_validation_issue",
    "validate_interface_validation_metadata",
    "validate_interface_validation_policy",
    "validate_interface_validation_record",
    "validate_interface_version_compatibility_rule",
    "validation_result_to_outcome",
]
