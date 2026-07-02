# Garuda

Garuda is the Operating System for Human Intelligence.

This repository is the monorepo foundation for Project Garuda. GAR-SPRINT-0001 authorizes only the engineering foundation: repository structure, development documentation, baseline tooling, tests, Docker and CI/CD preparation, health/version surfaces, logging, observability and developer experience.

No intelligence, trading, broker integration, portfolio management, authentication, knowledge graph, memory, decision engine or database design is implemented in this sprint.

## Source of Truth

The governing architecture documents are `GAR-0001` through `GAR-0015` and `GAR-SPRINT-0001`.

Implementation must remain traceable to those documents. Architectural ambiguity must be resolved before code is added.

## Current Sprint

- Sprint: GAR-SPRINT-0001
- Version: 2.0
- Status: Foundation implementation in progress
- Current task: Mission Charlie - Backend Skeleton

## Repository Foundation

This foundation provides:

- Repository governance files
- Monorepo directory skeleton
- README documentation in every directory
- Repository foundation validation tests
- Sprint status documentation

## Quick Start

### One-command setup

```bash
make bootstrap
```

### Start the app locally

```bash
make backend
```

```bash
make frontend
```

### Run the full validation suite

```bash
make test
```

```bash
make lint
```

```bash
make format
```

A minimal FastAPI backend shell is now available under services/backend with health and version endpoints, structured logging, request ID/error middleware, startup/shutdown lifecycle hooks, CORS support and OpenAPI generation. A minimal Next.js frontend shell is also available under apps/web with a landing dashboard, environment-based configuration, typed API client helpers, integration and smoke tests, and a live backend connection. Local Docker packaging for the backend and frontend is now included for development use, while CI/CD remains out of scope for this sprint.

For the full onboarding walkthrough, see [docs/developer-onboarding.md](docs/developer-onboarding.md).

## Architecture Discipline

Garuda is modular, observable, explainable, secure, documented and testable. Every component must have one clear responsibility and must avoid hidden business logic.

