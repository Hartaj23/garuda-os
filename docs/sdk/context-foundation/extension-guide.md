# Context Foundation SDK Extension Guide

## Extension Principles

Extensions must preserve the current Context Foundation boundaries:

- Platform Core remains the source of object identity and validation contracts.
- Context contracts remain descriptive until a later approved mission implements behavior.
- Context references remain service-independent and infrastructure-independent.
- Production behavior must not be inferred from SDK documentation.

## Additive Documentation

When new Context functionality is approved and implemented, update this SDK documentation after the
repository contains the actual APIs.

Before documenting new behavior, verify:

- the public export exists in `packages.context`
- tests cover the behavior
- architecture and engineering docs exist
- examples use implemented APIs only

## Extending Context Objects

Future extensions to Context objects should use Platform Core hooks and constructor patterns already
used by `UniversalContext`.

Do not introduce a separate object base class, serializer, validation engine, or lifecycle engine
from SDK documentation.

## Extending Contracts

Future contract additions should remain deterministic, immutable, and descriptive unless a later
approved mission explicitly implements behavior.

Current contracts:

- `ContextComposition`
- `ContextCompositionContract`
- `ContextSelectionRequest`
- `ContextSelectionContract`

These current contracts do not execute.

## Extending Runtime Containers

`ContextWorkspace` is runtime-only and process-local. Future storage, persistence, retrieval,
search, indexing, caching, distribution, or database behavior must be implemented by a separately
approved subsystem before it is documented as available.

## Documentation Review Checklist

- Examples import only from implemented packages.
- Links point to files in this repository.
- Future architecture is labeled as future architecture.
- No unimplemented Context engine behavior is described as available.
- Platform Core, Memory Foundation, and Knowledge Foundation dependency direction remains intact.
