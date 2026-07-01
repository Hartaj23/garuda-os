"""Validate the GAR-SPRINT-0001 repository foundation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    ".editorconfig",
    "CODEOWNERS",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/task.md",
    ".github/ISSUE_TEMPLATE/architecture-review.md",
]

REQUIRED_DIRECTORIES = [
    "docs",
    "docs/architecture",
    "docs/engineering",
    "docs/sprints",
    "apps",
    "apps/web",
    "apps/desktop",
    "services",
    "packages",
    "agents",
    "infrastructure",
    "scripts",
    "tests",
    ".github",
    ".github/ISSUE_TEMPLATE",
]


def missing_required_files() -> list[str]:
    return [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]


def missing_required_directories() -> list[str]:
    return [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]


def directories_without_readme() -> list[str]:
    missing = []
    for path in REQUIRED_DIRECTORIES:
        directory = ROOT / path
        if directory.is_dir() and not (directory / "README.md").is_file():
            missing.append(path)
    return missing


def validate() -> None:
    failures = {
        "missing files": missing_required_files(),
        "missing directories": missing_required_directories(),
        "directories without README.md": directories_without_readme(),
    }
    failed = {name: values for name, values in failures.items() if values}
    if failed:
        details = "; ".join(f"{name}: {', '.join(values)}" for name, values in failed.items())
        raise AssertionError(details)


if __name__ == "__main__":
    validate()
    print("Repository foundation validation passed.")

