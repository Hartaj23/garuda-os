# Knowledge Foundation Developer Guide

## Create Universal Knowledge

```python
from packages.knowledge import KnowledgeType, UniversalKnowledge

knowledge = UniversalKnowledge(
    knowledge_type=KnowledgeType.FACT,
)
```

`UniversalKnowledge` inherits Platform Core identity, metadata, tags, lifecycle state, audit
fields, validation hooks, behaviors, and relationship storage.

## Use Confidence And Metadata

```python
from packages.knowledge import KnowledgeConfidence, KnowledgeMetadata, KnowledgeState

knowledge = UniversalKnowledge(
    knowledge_type=KnowledgeType.CONCEPT,
    knowledge_state=KnowledgeState.SUPPORTED,
    confidence=KnowledgeConfidence(level="medium", rationale="documented"),
    knowledge_metadata=KnowledgeMetadata(values={"domain": "platform"}),
)
```

`KnowledgeConfidence` records trust supported by available context. It does not determine truth.

## Add Evidence And Provenance

```python
from datetime import datetime

from packages.knowledge import (
    EvidenceReference,
    EvidenceType,
    KnowledgeEvidence,
    KnowledgeOrigin,
    KnowledgeProvenance,
)

reference = EvidenceReference(
    reference_type=EvidenceType.DOCUMENT_REFERENCE,
    reference_identifier="GAR-SPRINT-0004",
)
evidence = KnowledgeEvidence(references=(reference,))
provenance = KnowledgeProvenance(
    origin=KnowledgeOrigin.HUMAN_CURATION,
    creator="codex",
    created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
    evidence_references=(reference,),
)

knowledge = UniversalKnowledge(
    knowledge_type=KnowledgeType.FACT,
    evidence=evidence,
    provenance=provenance,
)
```

Evidence references are opaque identifiers. They do not resolve external records or hold live
handles.

## Validate Knowledge

```python
result = knowledge.validate()

assert result.is_valid
```

Validation reuses Platform Core `ValidationResult` and merges Knowledge-specific validation
through the existing validation hook path.

## Serialize Knowledge

```python
payload = knowledge.to_dict()

assert payload["object_type"] == "UniversalKnowledge"
assert payload["knowledge_type"] == "fact"
```

`UniversalKnowledge.to_dict()` is the deterministic Knowledge payload. Platform Core
`ObjectSerializer` also works for inherited object fields.

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(knowledge)

assert core_payload["object_type"] == "UniversalKnowledge"
```

## Use Classification Contracts

```python
from packages.knowledge import (
    ClassificationDimension,
    KnowledgeCategory,
    KnowledgeClassificationContract,
)

classification_contract = KnowledgeClassificationContract(
    supported_categories=(KnowledgeCategory.FACTUAL,),
    supported_dimensions=(ClassificationDimension("domain"),),
)
```

Classification contracts describe supported categories and dimensions. They do not classify
Knowledge.

## Use Query Contracts

```python
from packages.knowledge import KnowledgeQuery, QueryConstraint, QueryType

query = KnowledgeQuery(
    query_type=QueryType.CATEGORY,
    constraints=(QueryConstraint("category", "equals", "factual"),),
)
```

Query contracts describe intent only. They do not execute, search, filter, rank, or retrieve.

## Use The Reference Store

```python
from packages.knowledge import KnowledgeReferenceStore

store = KnowledgeReferenceStore()
store.add(knowledge)

same_knowledge = store.get(knowledge.object_id)
identifiers = store.identifiers()
removed = store.remove(knowledge.object_id)
```

`KnowledgeReferenceStore` is process-local and in-memory only. It supports exact identifier lookup
and does not persist data.
