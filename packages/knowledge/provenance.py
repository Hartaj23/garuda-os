from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from .evidence import EvidenceReference


class KnowledgeOrigin(StrEnum):
    VALIDATED_MEMORY = "validated_memory"
    VERIFIED_OBSERVATION = "verified_observation"
    EXTERNAL_REFERENCE = "external_reference"
    HUMAN_CURATION = "human_curation"
    SYSTEM_FACT = "system_fact"


@dataclass(frozen=True, slots=True)
class KnowledgeProvenance:
    origin: KnowledgeOrigin
    creator: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    evidence_references: tuple[EvidenceReference, ...] = ()
    provenance_metadata: dict[str, Any] | tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_references", tuple(self.evidence_references))
        if isinstance(self.provenance_metadata, dict):
            object.__setattr__(
                self,
                "provenance_metadata",
                tuple(sorted(self.provenance_metadata.items())),
            )
        elif isinstance(self.provenance_metadata, tuple):
            object.__setattr__(
                self,
                "provenance_metadata",
                tuple(sorted(self.provenance_metadata)),
            )
        else:
            raise ValueError("provenance_metadata must be a dictionary or tuple")

    def to_dict(self) -> dict[str, object]:
        return {
            "origin": self.origin.value,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "evidence_references": [
                reference.to_dict() for reference in self.evidence_references
            ],
            "provenance_metadata": dict(self.provenance_metadata),
        }
