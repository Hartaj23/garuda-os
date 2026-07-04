# Knowledge Query Contract

## Scope

This document describes GAR-SPRINT-0004 Mission Echo: the Knowledge Query Contract.

Mission Echo defines immutable, descriptive contracts for representing Knowledge query intent. It
does not execute queries, search Knowledge, retrieve Knowledge, filter results, rank results or
perform semantic lookup.

## Package structure

The implementation lives in `packages/knowledge/query.py` and is exported through
`packages/knowledge/__init__.py`.

## Public interfaces

- `QueryType`
- `QueryConstraint`
- `QueryMetadata`
- `KnowledgeQuery`
- `KnowledgeQueryContract`
- `validate_query_metadata`
- `validate_query_constraint`
- `validate_knowledge_query`
- `validate_knowledge_query_contract`

## Query contract

`QueryType` is a platform-neutral enum describing query intent. `QueryConstraint` records one
constraint type, operator, value and metadata. `KnowledgeQuery` combines query type, constraints
and metadata into an immutable intent payload.

`KnowledgeQueryContract` records supported query types, supported constraint types, metadata and a
contract version. It describes what future systems may support. It does not execute or resolve
queries.

## Validation model

Mission Echo provides local validation helpers that return Platform Core `ValidationResult`
instances. The helpers validate structure only. They do not evaluate constraints or execute query
logic.

## Serialization compatibility

Query models expose deterministic `to_dict()` payloads. Mission Echo does not introduce a query
serializer and does not modify `ObjectSerializer`.

## Constitutional boundaries

The contract remains service-independent and infrastructure-independent. Platform Core and Memory
Foundation packages are unchanged. Existing Knowledge Foundation contracts remain intact.

## Explicitly out of scope

- Query execution
- Search
- Retrieval
- Filtering
- Ranking
- Semantic lookup
- Semantic search
- Reasoning
- Inference
- Persistence
- AI behavior
- REST APIs
- Frontend features
- Workflow behavior
