"""Minimal FastAPI backend application for GAR-SPRINT-0001."""

from __future__ import annotations

import json
import logging
import os
import uuid
from contextlib import asynccontextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

REQUEST_ID: ContextVar[str | None] = ContextVar("request_id", default=None)


@dataclass(slots=True)
class Settings:
    """Runtime settings for the backend shell."""

    app_name: str = "garuda"
    environment: str = "development"
    log_level: str = "INFO"
    version: str = "0.1.0a0"
    allowed_origins: tuple[str, ...] = ("http://localhost:3000",)


class StructuredJsonFormatter(logging.Formatter):
    """Format log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        request_id = REQUEST_ID.get()
        if request_id:
            payload["request_id"] = request_id
        for key, value in record.__dict__.items():
            if key in {
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
                "taskName",
            }:
                continue
            payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, sort_keys=True)


class RequestIdFilter(logging.Filter):
    """Attach the current request ID to each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = REQUEST_ID.get() or ""
        return True


def configure_logging(log_level: str) -> logging.Logger:
    logger = logging.getLogger("garuda.backend")
    logger.setLevel(log_level.upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredJsonFormatter())
        handler.addFilter(RequestIdFilter())
        logger.addHandler(handler)

    return logger


def load_settings() -> Settings:
    """Load settings from environment variables with safe defaults."""

    origins = tuple(
        origin.strip()
        for origin in os.getenv("GARUDA_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    )

    return Settings(
        app_name=os.getenv("GARUDA_APP_NAME", "garuda"),
        environment=os.getenv("GARUDA_ENVIRONMENT", "development"),
        log_level=os.getenv("GARUDA_LOG_LEVEL", "INFO"),
        version=os.getenv("GARUDA_VERSION", "0.1.0a0"),
        allowed_origins=origins,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = app.state.logger
    logger.info("application_startup", extra={"event": "startup"})
    yield
    logger.info("application_shutdown", extra={"event": "shutdown"})


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a FastAPI application with the required shell middleware and routes."""

    resolved_settings = settings or load_settings()
    logger = configure_logging(resolved_settings.log_level)

    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.version,
        lifespan=lifespan,
        openapi_url="/openapi.json",
    )
    app.state.settings = resolved_settings
    app.state.logger = logger

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(resolved_settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        token = REQUEST_ID.set(request_id)
        response = None
        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "request_failed",
                extra={
                    "event": "request_error",
                    "method": request.method,
                    "path": request.url.path,
                },
            )
            raise
        finally:
            REQUEST_ID.reset(token)
        response.headers["x-request-id"] = request_id
        return response

    @app.middleware("http")
    async def error_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:  # pragma: no cover - exercised through runtime behavior
            logger.exception(
                "unhandled_error",
                extra={
                    "event": "error",
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                },
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_server_error",
                    "detail": "An unexpected error occurred.",
                },
            )

    @app.get("/health")
    async def health() -> dict[str, str]:
        logger.info("health_check", extra={"event": "health"})
        return {"status": "ok"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {"version": resolved_settings.version}

    return app


app = create_app()
