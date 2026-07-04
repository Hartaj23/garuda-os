from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult


class KnowledgeType(StrEnum):
    FACT = "fact"
    CONCEPT = "concept"
    PRINCIPLE = "principle"
    RULE = "rule"
    OBSERVATION = "observation"


class KnowledgeState(StrEnum):
    DRAFT = "draft"
    SUPPORTED = "supported"
    VALIDATED = "validated"
    ESTABLISHED = "established"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class KnowledgeConfidence:
    level: str = "unknown"
    rationale: str | None = None

    def __post_init__(self) -> None:
        if self.level not in {"unknown", "low", "medium", "high"}:
            raise ValueError("level must be one of: unknown, low, medium, high")

    def to_dict(self) -> dict[str, str | None]:
        return {
            "level": self.level,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class KnowledgeMetadata:
    values: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.values, dict):
            object.__setattr__(self, "values", tuple(sorted(self.values.items())))
        elif isinstance(self.values, tuple):
            object.__setattr__(self, "values", tuple(sorted(self.values)))
        else:
            raise ValueError("values must be a dictionary or tuple of key-value pairs")

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


class UniversalKnowledge(CanonicalObject):
    """Platform-level knowledge object for GAR-SPRINT-0004 Mission Alpha."""

    def __init__(
        self,
        knowledge_type: KnowledgeType,
        knowledge_state: KnowledgeState = KnowledgeState.DRAFT,
        confidence: KnowledgeConfidence | None = None,
        knowledge_metadata: KnowledgeMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._knowledge_type = knowledge_type
        self._knowledge_state = knowledge_state
        self._confidence = confidence or KnowledgeConfidence()
        self._knowledge_metadata = knowledge_metadata or KnowledgeMetadata()
        self.register_validation_hook(validate_knowledge)

    @property
    def knowledge_type(self) -> KnowledgeType:
        return self._knowledge_type

    @property
    def knowledge_state(self) -> KnowledgeState:
        return self._knowledge_state

    @property
    def confidence(self) -> KnowledgeConfidence:
        return self._confidence

    @property
    def knowledge_metadata(self) -> KnowledgeMetadata:
        return self._knowledge_metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "object_version": self.object_version,
            "object_type": self.object_type,
            "object_id": str(self.object_id),
            "metadata": dict(sorted(self.metadata.values.items())),
            "tags": list(self.tags),
            "lifecycle_state": self.lifecycle_state.value,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "knowledge_type": self.knowledge_type.value,
            "knowledge_state": self.knowledge_state.value,
            "confidence": self.confidence.to_dict(),
            "knowledge_metadata": self.knowledge_metadata.to_dict(),
        }


def validate_knowledge(obj: UniversalKnowledge) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "knowledge_type", None), KnowledgeType):
        result.add_error(
            "Knowledge type must be a KnowledgeType value.",
            ValidationCategory.SCHEMA,
            field="knowledge_type",
            code="invalid_knowledge_type",
        )

    if not isinstance(getattr(obj, "knowledge_state", None), KnowledgeState):
        result.add_error(
            "Knowledge state must be a KnowledgeState value.",
            ValidationCategory.LIFECYCLE,
            field="knowledge_state",
            code="invalid_knowledge_state",
        )

    confidence = getattr(obj, "confidence", None)
    if not isinstance(confidence, KnowledgeConfidence):
        result.add_error(
            "Knowledge confidence must be a KnowledgeConfidence value.",
            ValidationCategory.METADATA,
            field="confidence",
            code="invalid_knowledge_confidence",
        )

    if not isinstance(getattr(obj, "knowledge_metadata", None), KnowledgeMetadata):
        result.add_error(
            "Knowledge metadata must be a KnowledgeMetadata value.",
            ValidationCategory.METADATA,
            field="knowledge_metadata",
            code="invalid_knowledge_metadata",
        )

    return result
