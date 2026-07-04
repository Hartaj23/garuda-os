# Knowledge Foundation SDK Practical Examples

## Create Knowledge

```python
from packages.knowledge import KnowledgeType, UniversalKnowledge

knowledge = UniversalKnowledge(
    knowledge_type=KnowledgeType.FACT,
)
```

## Add Evidence And Provenance

```python
from datetime import datetime

from packages.knowledge import (
    EvidenceReference,
    EvidenceType,
    KnowledgeEvidence,
    KnowledgeOrigin,
    KnowledgeProvenance,
    KnowledgeType,
    UniversalKnowledge,
)

reference = EvidenceReference(
    reference_type=EvidenceType.DOCUMENT_REFERENCE,
    reference_identifier="GAR-SPRINT-0004",
)
knowledge = UniversalKnowledge(
    knowledge_type=KnowledgeType.FACT,
    evidence=KnowledgeEvidence(references=(reference,)),
    provenance=KnowledgeProvenance(
        origin=KnowledgeOrigin.HUMAN_CURATION,
        creator="codex",
        created_at=datetime.fromisoformat("2026-07-04T00:00:00+00:00"),
        evidence_references=(reference,),
    ),
)
```

## Validate Knowledge

```python
result = knowledge.validate()

assert result.is_valid
```

## Serialize Knowledge

```python
payload = knowledge.to_dict()

assert payload["object_type"] == "UniversalKnowledge"
assert payload["knowledge_type"] == "fact"
assert payload["evidence"]["references"][0]["reference_identifier"] == "GAR-SPRINT-0004"
```

## Serialize Platform Core Fields

```python
from packages.objects import ObjectSerializer

core_payload = ObjectSerializer.serialize(knowledge)

assert core_payload["object_type"] == "UniversalKnowledge"
assert core_payload["object_id"] == str(knowledge.object_id)
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

classification_payload = classification_contract.to_dict()

assert classification_payload["supported_categories"] == ["factual"]
```

## Use Query Contracts

```python
from packages.knowledge import KnowledgeQuery, QueryConstraint, QueryType

query = KnowledgeQuery(
    query_type=QueryType.CATEGORY,
    constraints=(QueryConstraint("category", "equals", "factual"),),
)

query_payload = query.to_dict()

assert query_payload["query_type"] == "category"
```

## Use The Knowledge Reference Store

```python
from packages.knowledge import KnowledgeReferenceStore

store = KnowledgeReferenceStore()
store.add(knowledge)

assert store.get(knowledge.object_id) is knowledge
assert store.identifiers() == (knowledge.object_id,)

removed = store.remove(knowledge.object_id)

assert removed is knowledge
```

## Certified End-To-End Knowledge Flow

```python
from packages.knowledge import (
    ClassificationDimension,
    KnowledgeCategory,
    KnowledgeClassificationContract,
    KnowledgeQuery,
    KnowledgeReferenceStore,
    QueryConstraint,
    QueryType,
)
from packages.objects import ObjectSerializer

validation = knowledge.validate()
knowledge_payload = knowledge.to_dict()
core_payload = ObjectSerializer.serialize(knowledge)

classification_contract = KnowledgeClassificationContract(
    supported_categories=(KnowledgeCategory.FACTUAL,),
    supported_dimensions=(ClassificationDimension("domain"),),
)
query = KnowledgeQuery(
    query_type=QueryType.EXACT_IDENTIFIER,
    constraints=(QueryConstraint("identifier", "equals", str(knowledge.object_id)),),
)

store = KnowledgeReferenceStore()
store.add(knowledge)
stored_knowledge = store.get(knowledge.object_id)
removed_knowledge = store.remove(knowledge.object_id)

assert validation.is_valid
assert knowledge_payload["object_type"] == "UniversalKnowledge"
assert core_payload["object_id"] == str(knowledge.object_id)
assert classification_contract.to_dict()["supported_categories"] == ["factual"]
assert query.to_dict()["query_type"] == "exact_identifier"
assert stored_knowledge is knowledge
assert removed_knowledge is knowledge
assert store.identifiers() == ()
```

This flow mirrors the certified Knowledge Foundation integration path. It uses only existing SDK
capabilities and does not require persistence, REST, database, search, query execution, retrieval
engine, workflow, AI, Context, Reasoning, Decision, Agent, trading, or portfolio functionality.
