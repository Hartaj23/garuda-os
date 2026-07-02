# Developer Onboarding

## Quick Start

1. Install Python 3.11+ and Node.js 20+.
2. Clone the repository and change into the repo root.
3. Run `make bootstrap` to create the local virtual environment and install the Python and web dependencies.
4. Start the backend with `make backend`.
5. Start the frontend with `make frontend`.
6. Open http://localhost:3000 to view the Garuda dashboard.

## Common Commands

- `make backend` — start the FastAPI backend shell on port 8000
- `make frontend` — start the Next.js frontend shell on port 3000
- `make dev` — prepare the local development environment
- `make test` — run the repository test suite
- `make lint` — run lint checks for Python and web code
- `make format` — run formatting checks for Python and web code

## Environment Variables

Set the following if you need to override local defaults:

- `GARUDA_ALLOWED_ORIGINS` — comma-separated CORS origins for the backend
- `GARUDA_APP_NAME`, `GARUDA_ENVIRONMENT`, `GARUDA_LOG_LEVEL`, `GARUDA_VERSION` — backend runtime settings
- `NEXT_PUBLIC_BACKEND_URL`, `NEXT_PUBLIC_ENVIRONMENT`, `NEXT_PUBLIC_APP_VERSION`, `NEXT_PUBLIC_ARCHITECTURE_VERSION`, `NEXT_PUBLIC_SPRINT_VERSION` — frontend settings

## CI behavior

GitHub Actions runs repository validation, backend tests, frontend tests, linting, formatting checks, and Docker static validation on pushes to the master branch and on pull requests. The workflow does not perform live Docker runtime execution unless the runner provides it.

## Notes

This sprint remains limited to the backend and frontend shells, local development ergonomics, and tests. Authentication, databases, integrations and AI features are intentionally excluded.
