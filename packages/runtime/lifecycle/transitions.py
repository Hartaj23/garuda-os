from __future__ import annotations

from typing import Final

from packages.objects import ValidationCategory, ValidationResult

from .states import RuntimeLifecycleState

ALLOWED_RUNTIME_LIFECYCLE_TRANSITIONS: Final[
    dict[RuntimeLifecycleState, frozenset[RuntimeLifecycleState]]
] = {
    RuntimeLifecycleState.DRAFT: frozenset(
        {
            RuntimeLifecycleState.ACTIVE,
            RuntimeLifecycleState.CLOSED,
        }
    ),
    RuntimeLifecycleState.ACTIVE: frozenset(
        {
            RuntimeLifecycleState.SUSPENDED,
            RuntimeLifecycleState.CLOSED,
        }
    ),
    RuntimeLifecycleState.SUSPENDED: frozenset(
        {
            RuntimeLifecycleState.ACTIVE,
            RuntimeLifecycleState.CLOSED,
        }
    ),
    RuntimeLifecycleState.CLOSED: frozenset(
        {
            RuntimeLifecycleState.ARCHIVED,
        }
    ),
    RuntimeLifecycleState.ARCHIVED: frozenset(),
}


def validate_runtime_lifecycle_transition(
    current_state: RuntimeLifecycleState,
    target_state: RuntimeLifecycleState,
    field_prefix: str = "runtime_lifecycle_transition",
) -> ValidationResult:
    """Validate descriptive lifecycle transition rules.

    Transition validation is architectural metadata only. It does not execute transitions,
    schedule progression, or perform runtime orchestration.
    """

    result = ValidationResult()

    allowed_targets = ALLOWED_RUNTIME_LIFECYCLE_TRANSITIONS.get(current_state, frozenset())
    if target_state not in allowed_targets:
        result.add_error(
            "Runtime lifecycle transition is not permitted by descriptive lifecycle rules.",
            ValidationCategory.LIFECYCLE,
            field=field_prefix,
            code="invalid_lifecycle_transition",
        )

    return result
