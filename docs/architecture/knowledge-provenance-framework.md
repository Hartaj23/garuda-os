# Knowledge Origin, Evidence and Provenance Framework

## Scope

This document describes GAR-SPRINT-0004 Mission Bravo: the descriptive Knowledge Origin,
Evidence and Provenance Framework.

Mission Bravo extends `UniversalKnowledge` with descriptive evidence and provenance payloads. It
does not implement evidence evaluation, evidence scoring, evidence ranking, evidence comparison,
truth determination, inference, reasoning, search, query execution, persistence, AI behavior,
REST endpoints, frontend behavior or workflow behavior.

## Included capabilities

- `KnowledgeOrigin`
- `EvidenceType`
- `EvidenceReference`
- `KnowledgeEvidence`
- `KnowledgeProvenance`
- Universal Knowledge evidence and provenance integration
- Knowledge-specific validation hook coverage for evidence and provenance
- Deterministic `to_dict` payload support

## Concept boundaries

Mission Bravo preserves three separate concepts:

- `KnowledgeOrigin` records where knowledge originated.
- `KnowledgeEvidence` records what supports the knowledge.
- `KnowledgeProvenance` records how the knowledge entered and evolved within Garuda.

These concepts are intentionally independent and are not merged into a single model.

## Evidence model

`EvidenceReference` is an opaque identifier model. It records a reference type, an identifier,
an optional label and deterministic metadata. It does not resolve references and does not hold
live handles to memory objects, external documents or infrastructure resources.

`KnowledgeEvidence` groups descriptive evidence references and evidence metadata. It does not
evaluate, score, rank, compare or determine truth.

## Provenance model

`KnowledgeProvenance` records origin, creator, creation timestamp, related evidence references
and provenance metadata. Provenance is descriptive history only. It does not compute lineage,
resolve provenance, verify provenance or interpret provenance.

## Dependency direction

The Knowledge package depends on Platform Core through `CanonicalObject` and validation hooks.
Mission Bravo does not modify Platform Core and does not modify the Memory Foundation.

Memory may be referenced by opaque identifiers only. Evidence models do not reference
`UniversalMemory` instances directly.

## Validation model

`UniversalKnowledge` continues to use the existing Platform Core validation hook mechanism.
Mission Bravo extends the existing knowledge validation hook to validate evidence and provenance
shape only.

## Serialization compatibility

`UniversalKnowledge.to_dict()` remains the deterministic cognitive payload surface. Mission Bravo
adds `evidence` and `provenance` keys without changing the Mission Alpha payload keys.

`ObjectSerializer` is unchanged and remains responsible for inherited Platform Core fields only.

## Explicitly out of scope

- Classification contracts
- Query contracts
- Knowledge stores
- Knowledge Graph
- Evidence evaluation
- Evidence scoring
- Evidence ranking
- Evidence comparison
- Provenance resolution
- Lineage computation
- Search
- Reasoning
- Inference
- AI behavior
- Persistence
- REST APIs
- Frontend features
- Workflow behavior
