# Reasoning Foundation SDK Extension Guide

## Extension Boundary

The implemented Reasoning Foundation can be extended only through future approved missions. Current
extension work should preserve the existing contracts and avoid changing Platform Core, Memory
Foundation, Knowledge Foundation, or Context Foundation behavior.

## Preserve Existing Payloads

Do not rename or reorder existing `UniversalReasoning.to_dict()` payload keys. If a future approved
mission adds optional fields, append them after existing fields and preserve constructor
compatibility.

## Keep Contracts Separate From Engines

Strategy and chain contracts are descriptive. Future execution systems, if approved separately,
should live outside these contract models and should not mutate the contract payloads.

## Keep References Opaque

Reasoning inputs and chain step references store identifiers only. Future reference resolution, if
approved separately, should not be hidden inside these value models.

## Keep Workspace Runtime-Only

`ReasoningWorkspace` is process-local and not serializable. Future persistent stores, caches,
databases, or retrieval systems must be separate components approved by architecture review.

## Validation Extensions

Current validation uses Platform Core `ValidationResult` and local validation helpers. Do not add a
Reasoning validation engine. Future approved validation additions should remain deterministic and
compatible with Platform Core validation contracts.

## Documentation Rule

Document only behavior implemented in the repository. Future reasoning engines, inference,
conclusion generation, planning, decision making, orchestration, AI integration, REST APIs,
frontend behavior, workflow behavior, and persistence must remain explicitly out of scope until
implemented by an approved mission.
