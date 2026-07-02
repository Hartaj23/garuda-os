"""Basic validation checks for the local Docker packaging."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    docker_files = [
        ROOT / "infrastructure" / "backend.Dockerfile",
        ROOT / "infrastructure" / "frontend.Dockerfile",
        ROOT / "docker-compose.yml",
    ]
    missing = [path.name for path in docker_files if not path.exists()]
    if missing:
        print(f"Missing docker files: {missing}")
        return 1

    docker_cmd: list[str] | None = None
    if shutil.which("docker"):
        version_result = subprocess.run(
            ["docker", "compose", "version"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if version_result.returncode == 0:
            docker_cmd = ["docker", "compose"]
    elif shutil.which("docker-compose"):
        docker_cmd = ["docker-compose"]

    if docker_cmd is None:
        print("Docker CLI is unavailable in this environment; skipping compose validation.")
        return 0

    result = subprocess.run(
        docker_cmd + ["config"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    print("Docker compose configuration validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
