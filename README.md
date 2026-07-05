# Garuda

Garuda is the Operating System for Human Intelligence.

This repository is the monorepo foundation for Project Garuda. It now includes the
GAR-SPRINT-0006 Universal Reasoning Foundation prepared for release as `v0.6.0-alpha`.

No intelligence, trading, broker integration, portfolio management, authentication, Knowledge
Graph, Context Engine, reasoning engine, Workflow Engine, query engine, retrieval engine, search
engine, persistence or database design is implemented in this release.

## Source Of Truth

The governing architecture documents are `GAR-0001` through `GAR-0016`, the approved sprint
documents, and the committed repository state.

Implementation must remain traceable to those documents. Architectural ambiguity must be resolved
before code is added.

## Current Release

- Release: `v0.6.0-alpha`
- Sprint: GAR-SPRINT-0006
- Status: Universal Reasoning Foundation release prepared pending tag approval
- Recommended tag: `v0.6.0-alpha`

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

## Knowledge Foundation

GAR-SPRINT-0004 delivers the service-independent Knowledge Foundation under `packages/knowledge`:

- Universal Knowledge Framework
- Knowledge Origin, Evidence and Provenance Framework
- Knowledge Serialization & Validation Integration
- Knowledge Classification Contract
- Knowledge Query Contract
- Knowledge Reference Store
- Knowledge Foundation SDK Documentation

## Context Foundation

GAR-SPRINT-0005 delivers the service-independent Context Foundation under `packages/context`:

- Universal Context Framework
- Context Source & Scope Framework
- Context Serialization & Validation Integration
- Context Composition Contract
- Context Selection Contract
- Context Workspace
- Platform Integration & Quality Certification
- Context Foundation SDK Documentation

## Universal Reasoning Foundation

GAR-SPRINT-0006 delivers the service-independent Universal Reasoning Foundation under
`packages/reasoning`:

- Universal Reasoning Framework
- Reasoning Input & Provenance Framework
- Reasoning Serialization & Validation Certification
- Reasoning Strategy Contract
- Reasoning Chain Contract
- Reasoning Workspace
- Platform Integration & Quality Certification
- Reasoning Foundation SDK Documentation

## Documentation

- [Platform Core SDK](docs/sdk/platform-core/README.md)
- [Memory Foundation SDK](docs/sdk/memory-foundation/README.md)
- [Knowledge Foundation SDK](docs/sdk/knowledge-foundation/README.md)
- [Context Foundation SDK](docs/sdk/context-foundation/README.md)
- [Reasoning Foundation SDK](docs/sdk/reasoning-foundation/README.md)
- [Sprint 2 Closure Report](docs/sprints/GAR-SPRINT-0002-closure-report.md)
- [Sprint 3 Closure Report](docs/sprints/GAR-SPRINT-0003-closure-report.md)
- [Sprint 4 Closure Report](docs/sprints/GAR-SPRINT-0004-closure-report.md)
- [Sprint 5 Closure Report](docs/sprints/GAR-SPRINT-0005-closure-report.md)
- [Sprint 6 Closure Report](docs/sprints/GAR-SPRINT-0006-closure-report.md)
- [v0.2.0-alpha Release Notes](docs/releases/v0.2.0-alpha.md)
- [v0.3.0-alpha Release Notes](docs/releases/v0.3.0-alpha.md)
- [v0.4.0-alpha Release Notes](docs/releases/v0.4.0-alpha.md)
- [v0.5.0-alpha Release Notes](docs/releases/v0.5.0-alpha.md)
- [v0.6.0-alpha Release Notes](docs/releases/v0.6.0-alpha.md)
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

Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation and Universal Reasoning
Foundation remain service-independent and domain-neutral. Persistence, REST endpoints, database
storage, event bus publishing, workflow execution, reasoning execution, inference, AI integration,
Knowledge Graph behavior, Context Engine behavior, query engines, retrieval engines, search
engines, trading systems and portfolio systems remain out of scope until explicitly approved in
future architecture and sprint work.
