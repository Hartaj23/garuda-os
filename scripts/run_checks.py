"""Run local validation checks for the Garuda foundation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


COMMANDS = [
    [sys.executable, "-m", "unittest", "discover", "tests"],
    [sys.executable, "scripts/validate_repository_foundation.py"],
    [sys.executable, "scripts/validate_toolchain.py"],
    [sys.executable, "scripts/validate_docker.py"],
]


def main() -> int:
    for command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
