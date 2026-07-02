"""Entrypoint for running the Garuda backend shell."""

from __future__ import annotations

import uvicorn

from services.backend.app import create_app, load_settings


def main() -> None:
    settings = load_settings()
    uvicorn.run(
        create_app(settings),
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
