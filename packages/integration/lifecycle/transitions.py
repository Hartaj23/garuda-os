from __future__ import annotations

from typing import Final

from packages.objects import ValidationCategory, ValidationResult

from .states import IntegrationLifecycleState

ALLOWED_INTEGRATION_LIFECYCLE_TRANSITIONS: Final[
    dict[IntegrationLifecycleState, frozenset[IntegrationLifecycleState]]
] = {
    IntegrationLifecycleState.DRAFT: frozenset(
        {
            IntegrationLifecycleState.ACTIVE,
            IntegrationLifecycleState.CLOSED,
        }
    ),
    IntegrationLifecycleState.ACTIVE: frozenset(
        {
            IntegrationLifecycleState.SUSPENDED,
            IntegrationLifecycleState.CLOSED,
        }
    ),
    IntegrationLifecycleState.SUSPENDED: frozenset(
        {
            IntegrationLifecycleState.ACTIVE,
            IntegrationLifecycleState.CLOSED,
        }
    ),
    IntegrationLifecycleState.CLOSED: frozenset(
        {
            IntegrationLifecycleState.ARCHIVED,
        }
    ),
    IntegrationLifecycleState.ARCHIVED: frozenset(),
}


def validate_integration_lifecycle_transition(
    current_state: IntegrationLifecycleState,
    target_state: IntegrationLifecycleState,
    field_prefix: str = "integration_lifecycle_transition",
) -> ValidationResult:
    """Validate descriptive lifecycle transition rules.

    Transition validation is architectural metadata only. It does not execute transitions,
    schedule progression, or perform runtime orchestration.
    """

    result = ValidationResult()

    allowed_targets = ALLOWED_INTEGRATION_LIFECYCLE_TRANSITIONS.get(current_state, frozenset())
    if target_state not in allowed_targets:
        result.add_error(
            "Integration lifecycle transition is not permitted by descriptive lifecycle rules.",
            ValidationCategory.LIFECYCLE,
            field=field_prefix,
            code="invalid_lifecycle_transition",
        )

    return result
