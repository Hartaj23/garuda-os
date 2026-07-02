# Backend Shell

## Purpose

Provides the first FastAPI-based backend shell for Garuda.

## Current Scope

- FastAPI application creation
- Startup and graceful shutdown hooks
- Environment-based configuration loading
- Structured JSON logging
- Request ID propagation middleware
- Error middleware
- Health and version endpoints
- OpenAPI generation

## Run Locally

```bash
source .venv/bin/activate
python3 -m services.backend.main
```

## Test

```bash
source .venv/bin/activate
python3 -m unittest discover tests
```
