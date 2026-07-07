from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationCategory, ValidationResult

from .metadata import RuntimeValidationMetadata, validate_runtime_validation_metadata
from .result import RuntimeValidationOutcome, validation_result_to_outcome


@dataclass(frozen=True, slots=True)
class RuntimeValidationReport:
    """Aggregated deterministic validation report for runtime artifact evaluation."""

    is_valid: bool
    outcomes: tuple[RuntimeValidationOutcome, ...]
    report_metadata: RuntimeValidationMetadata

    def __post_init__(self) -> None:
        object.__setattr__(self, "outcomes", tuple(self.outcomes))

    def to_dict(self) -> dict[str, object]:
        return {
            "is_valid": self.is_valid,
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
            "report_metadata": self.report_metadata.to_dict(),
        }


def build_runtime_validation_report(
    *results: ValidationResult,
    report_metadata: RuntimeValidationMetadata | None = None,
) -> RuntimeValidationReport:
    """Aggregate validation results into a deterministic runtime validation report."""

    outcomes = tuple(validation_result_to_outcome(result) for result in results)
    metadata = report_metadata or RuntimeValidationMetadata(
        values={"report_scope": "runtime", "outcome_count": len(outcomes)}
    )
    return RuntimeValidationReport(
        is_valid=all(outcome.is_valid for outcome in outcomes),
        outcomes=outcomes,
        report_metadata=metadata,
    )


def validate_runtime_validation_report(
    report: object,
    field_prefix: str = "validation_report",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(report, RuntimeValidationReport):
        result.add_error(
            "Validation report must be a RuntimeValidationReport value.",
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
    if not isinstance(report_metadata, RuntimeValidationMetadata):
        result.add_error(
            "Validation report metadata must be a RuntimeValidationMetadata value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.report_metadata",
            code="invalid_validation_report_metadata",
        )
    else:
        result.merge(
            validate_runtime_validation_metadata(
                report_metadata,
                field_prefix=f"{field_prefix}.report_metadata",
            )
        )

    return result
