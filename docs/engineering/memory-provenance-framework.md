# Memory Source & Provenance Framework Engineering Notes

## Implementation summary

Mission Bravo extends the service-independent package
[packages/memory](../../packages/memory).

## Modules

- [packages/memory/source.py](../../packages/memory/source.py) defines source and acquisition
  enums plus `MemorySource`.
- [packages/memory/provenance.py](../../packages/memory/provenance.py) defines
  `ProvenanceReference`, `ProvenanceMetadata`, and the strengthened `MemoryProvenance`.
- [packages/memory/core.py](../../packages/memory/core.py) keeps `UniversalMemory` integration and
  memory validation.

## Public interface

The package exports:

- `MemoryOrigin`
- `AcquisitionMethod`
- `AcquisitionChannel`
- `ProvenanceReference`
- `ProvenanceMetadata`
- `MemorySource`
- `MemoryProvenance`
- `UniversalMemory`

Mission Alpha imports from `packages.memory` remain valid.

## Design notes

- `ProvenanceReference` is an opaque identifier model only.
- `ProvenanceMetadata` is frozen and stores references as an immutable tuple.
- Existing `UniversalMemory` construction remains compatible when only `source` is supplied.
- Deterministic payload support remains available through existing `to_dict` methods.
- Platform Core packages are not modified.

## Testing

Mission Bravo coverage lives in
[tests/test_memory_provenance_framework.py](../../tests/test_memory_provenance_framework.py).

The tests verify enum values, defaults, immutable construction, optional opaque references,
Universal Memory integration, validation, and deterministic payload output.
