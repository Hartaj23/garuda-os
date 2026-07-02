# Universal Object Registry Engineering Notes

## Implementation summary

The registry lives in [packages/objects](../../packages/objects) and is limited to canonical object types.

## Design notes

- Registry registration requires a subclass of `CanonicalObject`.
- Registry lookup is available by type name or class.
- The factory placeholder remains inert and raises `NotImplementedError`.
