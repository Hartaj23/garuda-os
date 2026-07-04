# Knowledge Foundation SDK Best Practices

## Use Platform Core Identity

Allow `UniversalKnowledge` to inherit object identity from Platform Core unless a deterministic
test fixture requires an explicit UUID.

## Keep Evidence Opaque

Use `EvidenceReference.reference_identifier` as an opaque string. Do not treat it as a live handle,
file path, service client, or resolved object.

## Separate Evidence From Provenance

Use `KnowledgeEvidence` for what supports Knowledge. Use `KnowledgeProvenance` for how Knowledge
entered or evolved inside Garuda.

## Use Deterministic Payloads

Use `UniversalKnowledge.to_dict()` for the complete Knowledge payload. Use `ObjectSerializer` only
when inherited Platform Core fields are needed.

## Treat Contracts As Contracts

Classification contracts describe categories and dimensions. Query contracts describe intent.
They do not classify, execute, search, retrieve, filter, rank, infer, reason, or persist.

## Use The Reference Store For Runtime References Only

`KnowledgeReferenceStore` is useful for process-local references during runtime or tests. It is not
a database, cache, persistent store, search index, or retrieval engine.

## Validate Before Sharing Payloads

Call `knowledge.validate()` before handing Knowledge objects to downstream code. Validation reuses
Platform Core and Knowledge-specific hooks.

## Preserve Dependency Direction

Knowledge may depend on Platform Core. Memory and Platform Core do not depend on Knowledge. Keep
cross-foundation references opaque.

## Avoid Future Functionality Leakage

Do not document or build Context, Reasoning, Decision, Agent, AI, persistence, search, REST,
frontend, workflow, or graph behavior as part of the implemented Knowledge Foundation.
