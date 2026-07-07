# Garuda

Garuda is the Operating System for Human Intelligence.

This repository is the monorepo foundation for Project Garuda. It now includes the
GAR-SPRINT-0011 Integration Foundation released as `v0.11.0-alpha`.

No intelligence, trading, broker integration, portfolio management, authentication, Knowledge
Graph, Context Engine, reasoning engine, Workflow Engine, query engine, retrieval engine, search
engine, persistence or database design is implemented in this release.

## Source Of Truth

The governing architecture documents are `GAR-0001` through `GAR-0018`, the approved sprint
documents, and the committed repository state.

Implementation must remain traceable to those documents. Architectural ambiguity must be resolved
before code is added.

## Engineering Governance v1.0

Project Garuda uses Constitutional Engineering.

Before contributing to Project Garuda, begin with [`BOOTSTRAP.md`](BOOTSTRAP.md), then complete the repository bootstrap sequence:

1. `AGENTS.md`
2. `GARUDA_CONTEXT.md`
3. `GARUDA_WORKFLOW.md`
4. `GARUDA_GLOSSARY.md`
5. `GARUDA_NAVIGATION.md`
6. Applicable GAR Constitutions
7. Approved Sprint Mission

`GARUDA_NAVIGATION.md` is the engineering governance entry point. It links the constitutional layer, engineering layer, `PROMPTS.md`, and `templates/`.

The frozen baseline is recorded in [`ENGINEERING_GOVERNANCE_v1.0.md`](ENGINEERING_GOVERNANCE_v1.0.md).

See also [`docs/README.md`](docs/README.md) for the full governance layer index.

## Current Status

Project Garuda now includes an AI Engineering Governance layer that standardizes implementation
across AI coding agents.

## Current Release

- Release: `v0.11.0-alpha`
- Sprint: GAR-SPRINT-0011
- Status: Integration Foundation release published
- Tag: `v0.11.0-alpha`
- Previous release: `v0.10.0-alpha`

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

## Universal Decision Foundation

GAR-SPRINT-0007 delivers the service-independent Universal Decision Foundation under
`packages/decision`:

- Universal Decision Framework
- Decision Input & Provenance Framework
- Decision Serialization & Validation Certification
- Decision Strategy Contract
- Decision Chain Contract
- Decision Workspace
- Platform Integration & Quality Certification
- Universal Decision Foundation SDK Documentation

## Universal Action Foundation

GAR-SPRINT-0008 delivers the service-independent Universal Action Foundation under
`packages/action`:

- Universal Action Framework
- Action Input & Provenance Framework
- Action Serialization & Validation Certification
- Action Strategy Contract
- Action Chain Contract
- Action Workspace
- Platform Integration & Quality Certification
- Universal Action Foundation SDK Documentation

## Universal Execution Foundation

GAR-SPRINT-0009 delivers the service-independent Universal Execution Foundation under
`packages/execution`:

- Universal Execution Framework
- Execution Input & Provenance Framework
- Execution Serialization & Validation Certification
- Execution Strategy Contract
- Execution Chain Contract
- Execution Workspace
- Platform Integration & Quality Certification
- Universal Execution Foundation SDK Documentation

## Interface Foundation

GAR-SPRINT-0010 delivers the Interface Foundation under `packages/interface`:

- Interface Core
- Canonical Interface Contracts
- Interface Lifecycle and Boundary Model
- Translation Framework
- Validation Framework
- Interface Registry
- Interface Foundation Certification
- Interface Foundation SDK Documentation

## Integration Foundation

GAR-SPRINT-0011 delivers the Integration Foundation under `packages.integration`:

- Integration Core
- Integration Contracts
- Integration Lifecycle and Boundary Model
- Integration Relationship Framework
- Integration Validation Framework
- Integration Registry
- Integration Foundation Certification
- Integration Foundation SDK Documentation

## Documentation

- [Platform Core SDK](docs/sdk/platform-core/README.md)
- [Memory Foundation SDK](docs/sdk/memory-foundation/README.md)
- [Knowledge Foundation SDK](docs/sdk/knowledge-foundation/README.md)
- [Context Foundation SDK](docs/sdk/context-foundation/README.md)
- [Reasoning Foundation SDK](docs/sdk/reasoning-foundation/README.md)
- [Decision Foundation SDK](docs/sdk/decision-foundation/README.md)
- [Action Foundation SDK](docs/sdk/action-foundation/README.md)
- [Execution Foundation SDK](docs/sdk/execution-foundation/README.md)
- [Interface Foundation SDK](docs/sdk/interface/README.md)
- [Integration Foundation SDK](docs/sdk/integration/README.md)
- [Sprint 2 Closure Report](docs/sprints/GAR-SPRINT-0002-closure-report.md)
- [Sprint 3 Closure Report](docs/sprints/GAR-SPRINT-0003-closure-report.md)
- [Sprint 4 Closure Report](docs/sprints/GAR-SPRINT-0004-closure-report.md)
- [Sprint 5 Closure Report](docs/sprints/GAR-SPRINT-0005-closure-report.md)
- [Sprint 6 Closure Report](docs/sprints/GAR-SPRINT-0006-closure-report.md)
- [Sprint 7 Closure Report](docs/sprints/GAR-SPRINT-0007-closure-report.md)
- [Sprint 8 Closure Report](docs/sprints/GAR-SPRINT-0008-closure-report.md)
- [Sprint 9 Closure Report](docs/sprints/GAR-SPRINT-0009-closure-report.md)
- [Sprint 10 Closure Report](docs/sprints/GAR-SPRINT-0010-closure-report.md)
- [Sprint 11 Closure Report](docs/sprints/GAR-SPRINT-0011-closure.md)
- [v0.2.0-alpha Release Notes](docs/releases/v0.2.0-alpha.md)
- [v0.3.0-alpha Release Notes](docs/releases/v0.3.0-alpha.md)
- [v0.4.0-alpha Release Notes](docs/releases/v0.4.0-alpha.md)
- [v0.5.0-alpha Release Notes](docs/releases/v0.5.0-alpha.md)
- [v0.6.0-alpha Release Notes](docs/releases/v0.6.0-alpha.md)
- [v0.7.0-alpha Release Notes](docs/releases/v0.7.0-alpha.md)
- [v0.8.0-alpha Release Notes](docs/releases/v0.8.0-alpha.md)
- [v0.9.0-alpha Release Notes](docs/releases/v0.9.0-alpha.md)
- [v0.10.0-alpha Release Notes](docs/releases/v0.10.0-alpha.md)
- [v0.11.0-alpha Release Notes](docs/releases/v0.11.0-alpha.md)
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

Platform Core, Memory Foundation, Knowledge Foundation, Context Foundation, Universal Reasoning
Foundation, Universal Decision Foundation, Universal Action Foundation and Universal Execution
Foundation remain service-independent and domain-neutral.
Persistence, REST endpoints, database storage, event bus publishing, workflow execution, reasoning
execution, inference, decision execution, action execution, execution behavior, outcome computation,
scheduling, orchestration, AI integration, Knowledge Graph behavior, Context Engine behavior, query
engines, retrieval engines, search engines, trading systems and portfolio systems remain out of scope
until explicitly approved in future architecture and sprint work.
