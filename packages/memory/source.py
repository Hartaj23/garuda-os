from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MemoryOrigin(StrEnum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"
    IMPORTED = "imported"
    EXTERNAL_SERVICE = "external_service"
    SENSOR = "sensor"
    UNKNOWN = "unknown"


class AcquisitionMethod(StrEnum):
    CONVERSATION = "conversation"
    OBSERVATION = "observation"
    IMPORT = "import"
    API = "api"
    MANUAL_ENTRY = "manual_entry"
    SYSTEM_EVENT = "system_event"
    FILE_IMPORT = "file_import"


class AcquisitionChannel(StrEnum):
    CHAT = "chat"
    VOICE = "voice"
    DOCUMENT = "document"
    API = "api"
    EMAIL = "email"
    SENSOR = "sensor"
    INTERNAL_PLATFORM = "internal_platform"


@dataclass(slots=True)
class MemorySource:
    source_type: str
    source_identifier: str | None = None
    source_label: str | None = None
    source_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.source_metadata, dict):
            raise ValueError("source_metadata must be a dictionary")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "source_identifier": self.source_identifier,
            "source_label": self.source_label,
            "source_metadata": dict(sorted(self.source_metadata.items())),
        }
