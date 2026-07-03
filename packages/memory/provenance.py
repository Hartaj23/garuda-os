from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .source import (
    AcquisitionChannel,
    AcquisitionMethod,
    MemoryOrigin,
    MemorySource,
)


@dataclass(frozen=True, slots=True)
class ProvenanceReference:
    reference_type: str
    reference_identifier: str
    reference_label: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "reference_type": self.reference_type,
            "reference_identifier": self.reference_identifier,
            "reference_label": self.reference_label,
        }


@dataclass(frozen=True, slots=True)
class ProvenanceMetadata:
    acquisition_timestamp: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    origin: MemoryOrigin = MemoryOrigin.UNKNOWN
    acquisition_method: AcquisitionMethod = AcquisitionMethod.MANUAL_ENTRY
    acquisition_channel: AcquisitionChannel = AcquisitionChannel.INTERNAL_PLATFORM
    references: tuple[ProvenanceReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "references", tuple(self.references))

    def to_dict(self) -> dict[str, object]:
        return {
            "acquisition_timestamp": self.acquisition_timestamp.isoformat(),
            "origin": self.origin.value,
            "acquisition_method": self.acquisition_method.value,
            "acquisition_channel": self.acquisition_channel.value,
            "references": [reference.to_dict() for reference in self.references],
        }


@dataclass(slots=True)
class MemoryProvenance:
    source: MemorySource
    recorded_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    recorded_by: str | None = None
    trace_metadata: dict[str, object] = field(default_factory=dict)
    provenance_metadata: ProvenanceMetadata | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.trace_metadata, dict):
            raise ValueError("trace_metadata must be a dictionary")
        if self.provenance_metadata is None:
            self.provenance_metadata = ProvenanceMetadata(
                acquisition_timestamp=self.recorded_at,
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source.to_dict(),
            "recorded_at": self.recorded_at.isoformat(),
            "recorded_by": self.recorded_by,
            "trace_metadata": dict(sorted(self.trace_metadata.items())),
            "provenance_metadata": self.provenance_metadata.to_dict()
            if self.provenance_metadata
            else None,
        }
