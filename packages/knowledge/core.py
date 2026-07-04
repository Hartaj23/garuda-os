from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import CanonicalObject, ValidationCategory, ValidationResult

from .evidence import EvidenceReference, EvidenceType, KnowledgeEvidence
from .provenance import KnowledgeOrigin, KnowledgeProvenance


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
    """Platform-level knowledge object."""

    def __init__(
        self,
        knowledge_type: KnowledgeType,
        knowledge_state: KnowledgeState = KnowledgeState.DRAFT,
        confidence: KnowledgeConfidence | None = None,
        knowledge_metadata: KnowledgeMetadata | None = None,
        evidence: KnowledgeEvidence | None = None,
        provenance: KnowledgeProvenance | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._knowledge_type = knowledge_type
        self._knowledge_state = knowledge_state
        self._confidence = confidence or KnowledgeConfidence()
        self._knowledge_metadata = knowledge_metadata or KnowledgeMetadata()
        self._evidence = evidence or KnowledgeEvidence()
        self._provenance = provenance
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

    @property
    def evidence(self) -> KnowledgeEvidence:
        return self._evidence

    @property
    def provenance(self) -> KnowledgeProvenance | None:
        return self._provenance

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
            "evidence": self.evidence.to_dict(),
            "provenance": self.provenance.to_dict() if self.provenance else None,
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

    evidence = getattr(obj, "evidence", None)
    if not isinstance(evidence, KnowledgeEvidence):
        result.add_error(
            "Knowledge evidence must be a KnowledgeEvidence value.",
            ValidationCategory.METADATA,
            field="evidence",
            code="invalid_knowledge_evidence",
        )
    else:
        result.merge(validate_knowledge_evidence(evidence))

    provenance = getattr(obj, "provenance", None)
    if provenance is not None:
        if not isinstance(provenance, KnowledgeProvenance):
            result.add_error(
                "Knowledge provenance must be a KnowledgeProvenance value.",
                ValidationCategory.METADATA,
                field="provenance",
                code="invalid_knowledge_provenance",
            )
        else:
            result.merge(validate_knowledge_provenance(provenance))

    return result


def validate_knowledge_evidence(evidence: KnowledgeEvidence) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(evidence.references, tuple):
        result.add_error(
            "Knowledge evidence references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="evidence.references",
            code="invalid_knowledge_evidence_references",
        )
        return result

    for index, reference in enumerate(evidence.references):
        result.merge(validate_evidence_reference(reference, f"evidence.references[{index}]"))

    return result


def validate_evidence_reference(reference: object, field_prefix: str) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(reference, EvidenceReference):
        result.add_error(
            "Evidence references must be EvidenceReference values.",
            ValidationCategory.METADATA,
            field=field_prefix,
            code="invalid_evidence_reference",
        )
        return result

    if not isinstance(reference.reference_type, EvidenceType):
        result.add_error(
            "Evidence reference type must be an EvidenceType value.",
            ValidationCategory.METADATA,
            field=f"{field_prefix}.reference_type",
            code="invalid_evidence_reference_type",
        )

    if not isinstance(reference.reference_identifier, str) or not reference.reference_identifier:
        result.add_error(
            "Evidence reference identifier must be a non-empty string.",
            ValidationCategory.IDENTITY,
            field=f"{field_prefix}.reference_identifier",
            code="invalid_evidence_reference_identifier",
        )

    return result


def validate_knowledge_provenance(provenance: KnowledgeProvenance) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(provenance.origin, KnowledgeOrigin):
        result.add_error(
            "Knowledge provenance origin must be a KnowledgeOrigin value.",
            ValidationCategory.METADATA,
            field="provenance.origin",
            code="invalid_knowledge_origin",
        )

    if not hasattr(provenance.created_at, "isoformat"):
        result.add_error(
            "Knowledge provenance creation timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="provenance.created_at",
            code="invalid_knowledge_provenance_created_at",
        )

    if not isinstance(provenance.evidence_references, tuple):
        result.add_error(
            "Knowledge provenance evidence references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="provenance.evidence_references",
            code="invalid_knowledge_provenance_references",
        )
        return result

    for index, reference in enumerate(provenance.evidence_references):
        result.merge(
            validate_evidence_reference(
                reference,
                f"provenance.evidence_references[{index}]",
            )
        )

    return result
