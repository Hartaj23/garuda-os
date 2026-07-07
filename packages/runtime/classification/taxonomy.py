from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from packages.runtime.contracts.common import RuntimeContextReference
from packages.objects import ValidationCategory, ValidationResult

from .metadata import RuntimeClassificationMetadata, validate_runtime_classification_metadata


class RuntimeContextClassification(StrEnum):
    NEUTRAL = "neutral"
    DESCRIPTIVE = "descriptive"
    EXTERNAL_FACING = "external_facing"
    GOVERNED = "governed"
    ASSOCIATED = "associated"


@dataclass(frozen=True, slots=True)
class RuntimeContextClassificationHook:
    """Runtime context classification hook for descriptive taxonomy structures."""

    context_reference: RuntimeContextReference
    classification: RuntimeContextClassification
    classification_metadata: RuntimeClassificationMetadata | None = None

    def __post_init__(self) -> None:
        if self.classification_metadata is None:
            object.__setattr__(self, "classification_metadata", RuntimeClassificationMetadata())

    def to_dict(self) -> dict[str, object]:
        classification_metadata = self.classification_metadata or RuntimeClassificationMetadata()
        return {
            "context_reference": self.context_reference.to_dict(),
            "classification": self.classification.value,
            "classification_metadata": classification_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class RuntimeContextClassificationHookCollection:
    hooks: tuple[RuntimeContextClassificationHook, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "hooks", tuple(self.hooks))

    def to_dict(self) -> dict[str, object]:
        return {
            "hooks": [hook.to_dict() for hook in self.hooks],
        }


def validate_runtime_context_classification_hook(
    hook: object,
    field_prefix: str = "classification_hook",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(hook, RuntimeContextClassificationHook):
        result.add_error(
            "Classification hook must be a RuntimeContextClassificationHook value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_hook",
        )
        return result

    if not isinstance(hook.classification, RuntimeContextClassification):
        result.add_error(
            "Classification must be a RuntimeContextClassification value.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.classification",
            code="invalid_classification",
        )

    if (
        not isinstance(hook.context_reference.context_identifier, str)
        or not hook.context_reference.context_identifier
    ):
        result.add_error(
            "Context reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.context_reference.context_identifier",
            code="invalid_context_reference_identifier",
        )

    classification_metadata = hook.classification_metadata
    if classification_metadata is not None:
        result.merge(
            validate_runtime_classification_metadata(
                classification_metadata,
                field_prefix=f"{field_prefix}.classification_metadata",
            )
        )

    return result


def validate_runtime_context_classification_hook_collection(
    collection: object,
    field_prefix: str = "classification_hooks",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(collection, RuntimeContextClassificationHookCollection):
        result.add_error(
            "Classification hooks must be a RuntimeContextClassificationHookCollection value.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_classification_hook_collection",
        )
        return result

    if not isinstance(collection.hooks, tuple):
        result.add_error(
            "Classification hooks must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.hooks",
            code="invalid_classification_hook_collection_hooks",
        )
        return result

    for index, hook in enumerate(collection.hooks):
        result.merge(
            validate_runtime_context_classification_hook(
                hook,
                field_prefix=f"{field_prefix}.hooks[{index}]",
            )
        )

    return result
