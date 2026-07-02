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
- Current task: Task 1 - Repository Foundation

## Repository Foundation

This foundation provides:

- Repository governance files
- Monorepo directory skeleton
- README documentation in every directory
- Repository foundation validation tests
- Sprint status documentation

## Quick Start

Run the repository foundation validation:

```bash
python3 -m unittest discover tests
```

Run all current foundation checks:

```bash
python3 scripts/run_checks.py
```

Full application startup commands will be added only when the backend, frontend and Docker deliverables are implemented in later GAR-SPRINT-0001 tasks.

## Architecture Discipline

Garuda is modular, observable, explainable, secure, documented and testable. Every component must have one clear responsibility and must avoid hidden business logic.

