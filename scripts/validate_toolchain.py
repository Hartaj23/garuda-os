"""Validate Mission Bravo engineering toolchain configuration."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "pyproject.toml",
    "package.json",
    "pnpm-workspace.yaml",
    ".npmrc",
    ".prettierrc.json",
    ".prettierignore",
    "eslint.config.mjs",
    ".pre-commit-config.yaml",
    "Makefile",
    "docs/engineering/toolchain.md",
    "scripts/run_checks.py",
]

FORBIDDEN_FOUNDATION_PATHS = [
    "apps/web/package.json",
    "apps/web/app",
    "apps/web/pages",
    "services/api",
    "docker-compose.yml",
]


def missing_required_files() -> list[str]:
    return [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]


def forbidden_paths_present() -> list[str]:
    return [path for path in FORBIDDEN_FOUNDATION_PATHS if (ROOT / path).exists()]


def python_tooling_configured() -> bool:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return "[tool.black]" in text and "[tool.ruff]" in text and "[tool.ruff.lint]" in text


def node_tooling_configured() -> bool:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    dependencies = package.get("devDependencies", {})
    return (
        package.get("packageManager", "").startswith("pnpm@")
        and "eslint" in dependencies
        and "prettier" in dependencies
        and "lint:web" in scripts
        and "format:web" in scripts
    )


def validate() -> None:
    failures = {}
    missing = missing_required_files()
    if missing:
        failures["missing files"] = missing
    forbidden = forbidden_paths_present()
    if forbidden:
        failures["future sprint leakage"] = forbidden
    if not python_tooling_configured():
        failures["python tooling"] = "Black and Ruff must be configured in pyproject.toml"
    if not node_tooling_configured():
        failures["node tooling"] = "pnpm, ESLint and Prettier must be configured in package.json"
    if failures:
        raise AssertionError(failures)


if __name__ == "__main__":
    validate()
    print("Engineering toolchain validation passed.")
