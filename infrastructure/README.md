# infrastructure

## Purpose

Contains infrastructure definitions for Docker, deployment, monitoring, observability and security.

## Owner

Founding Team.

## Dependencies

Approved deployment and observability architecture.

## Related Documents

- GAR-0003A
- GAR-0004
- GAR-0011
- GAR-SPRINT-0001

## AI Implementation Notes

The current sprint includes only local Docker packaging for the backend and frontend shells. CI/CD remains out of scope.

## Local Docker Usage

```bash
docker compose up --build
```

Then open http://localhost:3000 for the frontend and use http://localhost:8000/health or http://localhost:8000/version for the backend.

