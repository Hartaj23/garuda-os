# Object Serialization

## Scope

This document describes the Mission Charlie JSON serialization and deserialization support for the Universal Object System.

## Contract

- Serialization is handled by a dedicated serializer rather than by object methods.
- Every payload includes a serialization header with versioning and object metadata.
- Deserialization ignores unknown fields while preserving required object state.

## Explicitly out of scope

- Database persistence
- File storage
- Relationship semantics
- Lifecycle event processing

## Relationship note

Relationship objects use the existing serializer contract and serialize through a minimal, deterministic payload that preserves immutable object IDs and relationship metadata.
