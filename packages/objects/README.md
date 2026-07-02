# Universal Object System

This package contains the platform-level object primitives and registry used by GAR-SPRINT-0002.

## Current scope

- Core object model from Mission Alpha
- Universal object registry for canonical object types only
- Inert factory placeholder interface
- JSON serialization and deserialization for object state
- Relationship objects that reference immutable object IDs only
- Lifecycle event definitions for Universal Objects
- Universal Object validation result, error, severity, category, and helper utilities

## Out of scope

- Persistence
- Event bus or publishing infrastructure
- Lifecycle event processing runtime
- Business-rule, trading, portfolio, AI, database, REST, frontend, workflow, knowledge graph, or
  memory validation
