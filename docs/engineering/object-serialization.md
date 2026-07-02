# Object Serialization Engineering Notes

## Implementation summary

The JSON serializer lives in [packages/objects/serialization.py](../../packages/objects/serialization.py) and operates as a separate contract for object-to-JSON and JSON-to-object conversion.

## Design notes

- Payloads include a serialization header with `serialization_version`, `schema_version`, `object_version`, and `object_type`.
- Deterministic output is produced by sorting object metadata and behaviors and by emitting a stable JSON encoding.
- Deserialization tolerates unknown fields while preserving the required object state.
