from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from packages.objects import (
    CanonicalObject,
    ValidationCategory,
    ValidationResult,
)

from .provenance import MemoryProvenance, ProvenanceMetadata, ProvenanceReference
from .source import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryOrigin,
    MemorySource,
)


class MemoryType(StrEnum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    DECLARATIVE = "declarative"


class MemoryConfidence(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class MemoryMetadata:
    values: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.values, dict):
            raise ValueError("values must be a dictionary")

    def to_dict(self) -> dict[str, Any]:
        return dict(sorted(self.values.items()))


class UniversalMemory(CanonicalObject):
    """Platform-level memory object for GAR-SPRINT-0003 Mission Alpha."""

    def __init__(
        self,
        memory_type: MemoryType,
        content: Any,
        source: MemorySource,
        provenance: MemoryProvenance | None = None,
        confidence: MemoryConfidence = MemoryConfidence.UNKNOWN,
        memory_metadata: MemoryMetadata | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._memory_type = memory_type
        self._content = content
        self._source = source
        self._provenance = provenance or MemoryProvenance(source=source)
        self._confidence = confidence
        self._memory_metadata = memory_metadata or MemoryMetadata()
        self.register_validation_hook(validate_memory)

    @property
    def memory_type(self) -> MemoryType:
        return self._memory_type

    @property
    def content(self) -> Any:
        return self._content

    @property
    def source(self) -> MemorySource:
        return self._source

    @property
    def provenance(self) -> MemoryProvenance:
        return self._provenance

    @property
    def confidence(self) -> MemoryConfidence:
        return self._confidence

    @property
    def memory_metadata(self) -> MemoryMetadata:
        return self._memory_metadata

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
            "memory_type": self.memory_type.value,
            "content": self.content,
            "source": self.source.to_dict(),
            "provenance": self.provenance.to_dict(),
            "confidence": self.confidence.value,
            "memory_metadata": self.memory_metadata.to_dict(),
        }


def validate_memory(obj: UniversalMemory) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(getattr(obj, "memory_type", None), MemoryType):
        result.add_error(
            "Memory type must be a MemoryType value.",
            ValidationCategory.SCHEMA,
            field="memory_type",
            code="invalid_memory_type",
        )

    if getattr(obj, "content", None) is None:
        result.add_error(
            "Memory content is required.",
            ValidationCategory.SCHEMA,
            field="content",
            code="missing_memory_content",
        )

    source = getattr(obj, "source", None)
    if not isinstance(source, MemorySource):
        result.add_error(
            "Memory source must be a MemorySource value.",
            ValidationCategory.METADATA,
            field="source",
            code="invalid_memory_source",
        )
    elif not isinstance(source.source_type, str) or not source.source_type:
        result.add_error(
            "Memory source type must be a non-empty string.",
            ValidationCategory.METADATA,
            field="source.source_type",
            code="invalid_memory_source_type",
        )

    provenance = getattr(obj, "provenance", None)
    if not isinstance(provenance, MemoryProvenance):
        result.add_error(
            "Memory provenance must be a MemoryProvenance value.",
            ValidationCategory.METADATA,
            field="provenance",
            code="invalid_memory_provenance",
        )
    elif not isinstance(provenance.source, MemorySource):
        result.add_error(
            "Memory provenance source must be a MemorySource value.",
            ValidationCategory.METADATA,
            field="provenance.source",
            code="invalid_memory_provenance_source",
        )
    else:
        provenance_metadata = getattr(provenance, "provenance_metadata", None)
        if not isinstance(provenance_metadata, ProvenanceMetadata):
            result.add_error(
                "Memory provenance metadata must be a ProvenanceMetadata value.",
                ValidationCategory.METADATA,
                field="provenance.provenance_metadata",
                code="invalid_memory_provenance_metadata",
            )
        else:
            result.merge(validate_provenance_metadata(provenance_metadata))

    if not isinstance(getattr(obj, "confidence", None), MemoryConfidence):
        result.add_error(
            "Memory confidence must be a MemoryConfidence value.",
            ValidationCategory.METADATA,
            field="confidence",
            code="invalid_memory_confidence",
        )

    if not isinstance(getattr(obj, "memory_metadata", None), MemoryMetadata):
        result.add_error(
            "Memory metadata must be a MemoryMetadata value.",
            ValidationCategory.METADATA,
            field="memory_metadata",
            code="invalid_memory_metadata",
        )

    return result


def validate_provenance_metadata(metadata: ProvenanceMetadata) -> ValidationResult:
    result = ValidationResult()

    if not hasattr(metadata.acquisition_timestamp, "isoformat"):
        result.add_error(
            "Provenance acquisition timestamp must be datetime-like.",
            ValidationCategory.METADATA,
            field="provenance.provenance_metadata.acquisition_timestamp",
            code="invalid_acquisition_timestamp",
        )

    if not isinstance(metadata.origin, MemoryOrigin):
        result.add_error(
            "Memory origin must be a MemoryOrigin value.",
            ValidationCategory.METADATA,
            field="provenance.provenance_metadata.origin",
            code="invalid_memory_origin",
        )

    if not isinstance(metadata.acquisition_method, AcquisitionMethod):
        result.add_error(
            "Acquisition method must be an AcquisitionMethod value.",
            ValidationCategory.METADATA,
            field="provenance.provenance_metadata.acquisition_method",
            code="invalid_acquisition_method",
        )

    if not isinstance(metadata.acquisition_channel, AcquisitionChannel):
        result.add_error(
            "Acquisition channel must be an AcquisitionChannel value.",
            ValidationCategory.METADATA,
            field="provenance.provenance_metadata.acquisition_channel",
            code="invalid_acquisition_channel",
        )

    if not isinstance(metadata.references, tuple):
        result.add_error(
            "Provenance references must be stored as an immutable tuple.",
            ValidationCategory.METADATA,
            field="provenance.provenance_metadata.references",
            code="invalid_provenance_references",
        )
    else:
        for index, reference in enumerate(metadata.references):
            if not isinstance(reference, ProvenanceReference):
                result.add_error(
                    "Provenance references must be ProvenanceReference values.",
                    ValidationCategory.METADATA,
                    field=f"provenance.provenance_metadata.references[{index}]",
                    code="invalid_provenance_reference",
                )
                continue
            if not isinstance(reference.reference_type, str) or not reference.reference_type:
                result.add_error(
                    "Provenance reference type must be a non-empty string.",
                    ValidationCategory.METADATA,
                    field=f"provenance.provenance_metadata.references[{index}].reference_type",
                    code="invalid_provenance_reference_type",
                )
            if (
                not isinstance(reference.reference_identifier, str)
                or not reference.reference_identifier
            ):
                result.add_error(
                    "Provenance reference identifier must be a non-empty string.",
                    ValidationCategory.METADATA,
                    field=(
                        "provenance.provenance_metadata."
                        f"references[{index}].reference_identifier"
                    ),
                    code="invalid_provenance_reference_identifier",
                )

    return result
