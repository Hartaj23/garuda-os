from __future__ import annotations

from dataclasses import dataclass

from packages.objects import ValidationResult

from .metadata import RuntimeClassificationMetadata
from .taxonomy import (
    RuntimeContextClassificationHook,
    validate_runtime_context_classification_hook,
)


@dataclass(frozen=True, slots=True)
class RuntimeContextClassificationEvaluation:
    """Deterministic descriptive runtime context classification evaluation result.

    Evaluation records architectural semantics only. It does not route messages, invoke providers,
    schedule progression, or perform operational runtime execution.
    """

    classification: str
    context_identifier: str
    evaluation_metadata: RuntimeClassificationMetadata

    def to_dict(self) -> dict[str, object]:
        return {
            "classification": self.classification,
            "context_identifier": self.context_identifier,
            "evaluation_metadata": self.evaluation_metadata.to_dict(),
        }


def evaluate_runtime_context_classification(
    hook: RuntimeContextClassificationHook,
) -> RuntimeContextClassificationEvaluation:
    """Evaluate descriptive runtime context classification semantics deterministically.

    Pure function: identical hook inputs always produce identical evaluation outputs.
    """

    validation = validate_runtime_context_classification_hook(hook)
    if not validation.is_valid:
        raise ValueError("Classification hook failed validation before evaluation.")

    return RuntimeContextClassificationEvaluation(
        classification=hook.classification.value,
        context_identifier=hook.context_reference.context_identifier,
        evaluation_metadata=RuntimeClassificationMetadata(
            values={
                "evaluation_scope": "descriptive",
                "classification": hook.classification.value,
            }
        ),
    )


def evaluate_runtime_context_classification_validation(
    hook: RuntimeContextClassificationHook,
) -> ValidationResult:
    return validate_runtime_context_classification_hook(hook)
