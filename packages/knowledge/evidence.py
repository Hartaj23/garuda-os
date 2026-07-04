from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EvidenceType(StrEnum):
    MEMORY_REFERENCE = "memory_reference"
    DOCUMENT_REFERENCE = "document_reference"
    EXTERNAL_REFERENCE = "external_reference"
    OBSERVATION_REFERENCE = "observation_reference"
    CERTIFIED_EVIDENCE = "certified_evidence"


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    reference_type: EvidenceType
    reference_identifier: str
    reference_label: str | None = None
    reference_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.reference_metadata, dict):
            object.__setattr__(
                self,
                "reference_metadata",
                tuple(sorted(self.reference_metadata.items())),
            )
        elif isinstance(self.reference_metadata, tuple):
            object.__setattr__(
                self,
                "reference_metadata",
                tuple(sorted(self.reference_metadata)),
            )
        else:
            raise ValueError("reference_metadata must be a dictionary or tuple")

    def to_dict(self) -> dict[str, object]:
        return {
            "reference_type": self.reference_type.value,
            "reference_identifier": self.reference_identifier,
            "reference_label": self.reference_label,
            "reference_metadata": dict(self.reference_metadata),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeEvidence:
    references: tuple[EvidenceReference, ...] = ()
    evidence_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))
        if isinstance(self.evidence_metadata, dict):
            object.__setattr__(
                self,
                "evidence_metadata",
                tuple(sorted(self.evidence_metadata.items())),
            )
        elif isinstance(self.evidence_metadata, tuple):
            object.__setattr__(
                self,
                "evidence_metadata",
                tuple(sorted(self.evidence_metadata)),
            )
        else:
            raise ValueError("evidence_metadata must be a dictionary or tuple")

    def to_dict(self) -> dict[str, object]:
        return {
            "references": [reference.to_dict() for reference in self.references],
            "evidence_metadata": dict(self.evidence_metadata),
        }
