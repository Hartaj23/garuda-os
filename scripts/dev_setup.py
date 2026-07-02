"""Developer convenience commands for the Garuda sprint shell."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd or ROOT, env=env, check=True)


def bootstrap() -> None:
    """Create the local virtualenv and install Python dependencies if missing."""
    venv_dir = ROOT / ".venv"
    if not venv_dir.exists():
        _run([sys.executable, "-m", "venv", str(venv_dir)])

    python_bin = venv_dir / "bin" / "python"
    if not python_bin.exists():
        raise RuntimeError("Virtual environment is missing its Python binary")

    _run([str(python_bin), "-m", "pip", "install", "--upgrade", "pip"])
    _run(
        [
            str(python_bin),
            "-m",
            "pip",
            "install",
            "fastapi>=0.115.0",
            "uvicorn>=0.30.0",
            "httpx>=0.27.0",
            "ruff>=0.8.0",
            "black>=24.0.0",
        ]
    )

    frontend_dir = ROOT / "apps" / "web"
    if not (frontend_dir / "node_modules").exists():
        _run(["npm", "install"], cwd=frontend_dir)


def start_backend() -> None:
    """Start the backend with a single command."""
    env = os.environ.copy()
    env.setdefault("GARUDA_ALLOWED_ORIGINS", "http://localhost:3000")
    _run(
        [
            str(ROOT / ".venv" / "bin" / "python"),
            "-m",
            "uvicorn",
            "services.backend.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        env=env,
    )


def start_frontend() -> None:
    """Start the frontend with a single command."""
    frontend_dir = ROOT / "apps" / "web"
    _run(["npm", "run", "dev"], cwd=frontend_dir)


def start_dev_environment() -> None:
    """Start the backend and frontend together."""
    bootstrap()
    print("Backend and frontend startup commands are available via the Makefile targets.")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 scripts/dev_setup.py <bootstrap|backend|frontend|dev>")

    command = sys.argv[1]
    if command == "bootstrap":
        bootstrap()
    elif command == "backend":
        start_backend()
    elif command == "frontend":
        start_frontend()
    elif command == "dev":
        start_dev_environment()
    else:
        raise SystemExit("Unknown command")


if __name__ == "__main__":
    main()
