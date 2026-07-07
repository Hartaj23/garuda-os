from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationResult

from .metadata import IntegrationValidationMetadata, validate_integration_validation_metadata
from .result import IntegrationValidationOutcome, validation_result_to_outcome


@dataclass(frozen=True, slots=True)
class IntegrationValidationReport:
    """Aggregated deterministic validation report for integration artifact evaluation."""

    is_valid: bool
    outcomes: tuple[IntegrationValidationOutcome, ...]
    report_metadata: IntegrationValidationMetadata

    def __post_init__(self) -> None:
        object.__setattr__(self, "outcomes", tuple(self.outcomes))

    def to_dict(self) -> dict[str, object]:
        return {
            "is_valid": self.is_valid,
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
            "report_metadata": self.report_metadata.to_dict(),
        }


def build_integration_validation_report(
    *results: ValidationResult,
    report_metadata: IntegrationValidationMetadata | None = None,
) -> IntegrationValidationReport:
    """Aggregate validation results into a deterministic integration validation report."""

    outcomes = tuple(validation_result_to_outcome(result) for result in results)
    metadata = report_metadata or IntegrationValidationMetadata(
        values={"report_scope": "integration", "outcome_count": len(outcomes)}
    )
    return IntegrationValidationReport(
        is_valid=all(outcome.is_valid for outcome in outcomes),
        outcomes=outcomes,
        report_metadata=metadata,
    )


def validate_integration_validation_report(
    report: object,
    field_prefix: str = "validation_report",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(report, IntegrationValidationReport):
        result.add_error(
            "Validation report must be an IntegrationValidationReport value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_validation_report",
        )
        return result

    if not isinstance(report.outcomes, tuple):
        result.add_error(
            "Validation report outcomes must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.outcomes",
            code="invalid_validation_report_outcomes",
        )

    report_metadata = report.report_metadata
    if not isinstance(report_metadata, IntegrationValidationMetadata):
        result.add_error(
            "Validation report metadata must be an IntegrationValidationMetadata value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.report_metadata",
            code="invalid_validation_report_metadata",
        )
    else:
        result.merge(
            validate_integration_validation_metadata(
                report_metadata,
                field_prefix=f"{field_prefix}.report_metadata",
            )
        )

    return result
