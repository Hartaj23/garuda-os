# Garuda

Garuda is the Operating System for Human Intelligence.

This repository is the monorepo foundation for Project Garuda. It now includes the
GAR-SPRINT-0003 Memory Foundation prepared for release as `v0.3.0-alpha`.

No intelligence, trading, broker integration, portfolio management, authentication, Knowledge
Graph, Workflow Engine, retrieval engine, persistence or database design is implemented in this
release.

## Source Of Truth

The governing architecture documents are `GAR-0001` through `GAR-0016`, the approved sprint
documents, and the committed repository state.

Implementation must remain traceable to those documents. Architectural ambiguity must be resolved
before code is added.

## Current Release

- Release: `v0.3.0-alpha`
- Sprint: GAR-SPRINT-0003
- Status: Memory Foundation release prepared pending tag approval
- Recommended tag: `v0.3.0-alpha`

## Platform Core

GAR-SPRINT-0002 delivers the service-independent Universal Object System under `packages/objects`:

- Universal Object Framework
- Universal Object Registry
- Serialization Framework
- Universal Relationship Framework
- Lifecycle Event Framework
- Validation Framework
- Platform Integration & Quality Certification
- Platform Core SDK Documentation

## Memory Foundation

GAR-SPRINT-0003 delivers the service-independent Memory Foundation under `packages/memory`:

- Universal Memory Framework
- Memory Source & Provenance Framework
- Memory Serialization & Validation Integration
- Memory Index Contract
- Memory Retrieval Contract
- In-Memory Reference Store
- Platform Integration & Quality Certification
- Memory Foundation SDK Documentation

## Documentation

- [Platform Core SDK](docs/sdk/platform-core/README.md)
- [Memory Foundation SDK](docs/sdk/memory-foundation/README.md)
- [Sprint 2 Closure Report](docs/sprints/GAR-SPRINT-0002-closure-report.md)
- [Sprint 3 Closure Report](docs/sprints/GAR-SPRINT-0003-closure-report.md)
- [v0.2.0-alpha Release Notes](docs/releases/v0.2.0-alpha.md)
- [v0.3.0-alpha Release Notes](docs/releases/v0.3.0-alpha.md)
- [Developer Onboarding](docs/developer-onboarding.md)

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

## Architecture Discipline

Garuda is modular, observable, explainable, secure, documented and testable. Every component must
have one clear responsibility and must avoid hidden business logic.

Platform Core and Memory Foundation remain service-independent and domain-neutral. Persistence,
REST endpoints, database storage, event bus publishing, workflow execution, AI reasoning,
Knowledge Graph behavior, retrieval engines, trading systems and portfolio systems remain out of
scope until explicitly approved in future architecture and sprint work.
