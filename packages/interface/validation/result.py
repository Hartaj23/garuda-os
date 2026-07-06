from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .errors import InterfaceValidationIssue, InterfaceValidationIssueCollection


@dataclass(frozen=True, slots=True)
class InterfaceValidationOutcome:
    is_valid: bool
    issues: InterfaceValidationIssueCollection

    def to_dict(self) -> dict[str, object]:
        return {
            "is_valid": self.is_valid,
            "issues": self.issues.to_dict()["issues"],
        }


def validation_result_to_outcome(result: ValidationResult) -> InterfaceValidationOutcome:
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
        InterfaceValidationIssue(
            field=error.field or "artifact",
            message=error.message,
        )
        for error in sorted_errors
    )
    return InterfaceValidationOutcome(
        is_valid=result.is_valid,
        issues=InterfaceValidationIssueCollection(issues=issues),
    )
