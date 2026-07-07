from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .errors import IntegrationValidationIssue, IntegrationValidationIssueCollection


@dataclass(frozen=True, slots=True)
class IntegrationValidationOutcome:
    is_valid: bool
    issues: IntegrationValidationIssueCollection

    def to_dict(self) -> dict[str, object]:
        return {
            "is_valid": self.is_valid,
            "issues": self.issues.to_dict()["issues"],
        }


def validation_result_to_outcome(result: ValidationResult) -> IntegrationValidationOutcome:
    sorted_errors = sorted(
        result.errors,
        key=lambda error: (
            error.field or "",
            error.code or "",
            error.message,
            error.category.value,
            error.severity.value,
        ),
    )
    issues = tuple(
        IntegrationValidationIssue(
            field=error.field or "artifact",
            message=error.message,
        )
        for error in sorted_errors
    )
    return IntegrationValidationOutcome(
        is_valid=result.is_valid,
        issues=IntegrationValidationIssueCollection(issues=issues),
    )


def serialize_integration_validation_outcome(
    outcome: IntegrationValidationOutcome,
) -> dict[str, object]:
    """Deterministic serialization of integration validation outcomes."""

    if not isinstance(outcome, IntegrationValidationOutcome):
        raise ValueError("Outcome must be an IntegrationValidationOutcome value.")

    return outcome.to_dict()
