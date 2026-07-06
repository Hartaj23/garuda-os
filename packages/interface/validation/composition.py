from __future__ import annotations

from packages.objects import ValidationResult


def compose_interface_validation_results(
    *results: ValidationResult,
) -> ValidationResult:
    """Compose validation results in explicit deterministic order.

    Evaluation order:
    1. First supplied result
    2. Each subsequent result in argument order
    """
    composed = ValidationResult()
    for result in results:
        composed.merge(result)
    return composed
