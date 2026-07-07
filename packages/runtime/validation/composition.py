from __future__ import annotations

from packages.objects import ValidationError, ValidationResult


def _validation_error_sort_key(error: ValidationError) -> tuple[str, str, str, str, str]:
    return (
        error.field or "",
        error.code or "",
        error.message,
        error.category.value,
        error.severity.value,
    )


def compose_runtime_validation_results(
    *results: ValidationResult,
) -> ValidationResult:
    """Compose validation results with stable merged issue ordering.

    Evaluation order:
    1. Merge each supplied result in argument order
    2. Reorder merged issues using a deterministic sort key so equivalent issue sets
       produce identical ordering regardless of input result sequence

    Stable ordering invariant:
    Issues are sorted by (field, code, message, category, severity). Calling this function
    with the same set of issues in any input order yields the same merged issue sequence.
    """
    composed = ValidationResult()
    for result in results:
        composed.merge(result)
    composed.errors = sorted(composed.errors, key=_validation_error_sort_key)
    return composed
