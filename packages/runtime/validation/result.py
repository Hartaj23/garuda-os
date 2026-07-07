from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .errors import RuntimeValidationIssue, RuntimeValidationIssueCollection


@dataclass(frozen=True, slots=True)
class RuntimeValidationOutcome:
    is_valid: bool
    issues: RuntimeValidationIssueCollection

    def to_dict(self) -> dict[str, object]:
        return {
            "is_valid": self.is_valid,
            "issues": self.issues.to_dict()["issues"],
        }


def validation_result_to_outcome(result: ValidationResult) -> RuntimeValidationOutcome:
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
        RuntimeValidationIssue(
            field=error.field or "artifact",
            message=error.message,
        )
        for error in sorted_errors
    )
    return RuntimeValidationOutcome(
        is_valid=result.is_valid,
        issues=RuntimeValidationIssueCollection(issues=issues),
    )


def serialize_runtime_validation_outcome(
    outcome: RuntimeValidationOutcome,
) -> dict[str, object]:
    """Deterministic serialization of runtime validation outcomes."""

    if not isinstance(outcome, RuntimeValidationOutcome):
        raise ValueError("Outcome must be a RuntimeValidationOutcome value.")

    return outcome.to_dict()
