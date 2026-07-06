from __future__ import annotations

from dataclasses import dataclass, field

from packages.objects import ValidationCategory, ValidationResult

from .metadata import InterfaceValidationMetadata, validate_interface_validation_metadata


@dataclass(frozen=True, slots=True)
class InterfaceValidationIssue:
    """Structural validation issue only — no business or transport semantics."""

    field: str
    message: str
    issue_metadata: InterfaceValidationMetadata | None = None

    def __post_init__(self) -> None:
        if self.issue_metadata is None:
            object.__setattr__(self, "issue_metadata", InterfaceValidationMetadata())

    def to_dict(self) -> dict[str, object]:
        issue_metadata = self.issue_metadata or InterfaceValidationMetadata()
        return {
            "field": self.field,
            "message": self.message,
            "issue_metadata": issue_metadata.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterfaceValidationIssueCollection:
    issues: tuple[InterfaceValidationIssue, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "issues", tuple(self.issues))

    def to_dict(self) -> dict[str, object]:
        return {
            "issues": [issue.to_dict() for issue in self.issues],
        }


def validate_interface_validation_issue(
    issue: object,
    field_prefix: str = "validation_issue",
) -> ValidationResult:
    result = ValidationResult()

    if not isinstance(issue, InterfaceValidationIssue):
        result.add_error(
            "Validation issue must be an InterfaceValidationIssue value.",
            ValidationCategory.SCHEMA,
            field=field_prefix,
            code="invalid_validation_issue",
        )
        return result

    if not isinstance(issue.field, str) or not issue.field:
        result.add_error(
            "Validation issue field must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.field",
            code="invalid_validation_issue_field",
        )

    if not isinstance(issue.message, str) or not issue.message:
        result.add_error(
            "Validation issue message must be a non-empty string.",
            ValidationCategory.SCHEMA,
            field=f"{field_prefix}.message",
            code="invalid_validation_issue_message",
        )

    issue_metadata = issue.issue_metadata
    if issue_metadata is not None:
        result.merge(
            validate_interface_validation_metadata(
                issue_metadata,
                field_prefix=f"{field_prefix}.issue_metadata",
            )
        )

    return result
