from __future__ import annotations

from packages.interface.contracts.common import CanonicalInterfacePayload

from .representation import ExternalRepresentation


def normalize_to_canonical_payload(
    representation: ExternalRepresentation,
) -> CanonicalInterfacePayload:
    """Pure architectural transformation from external representation to canonical payload.

    Translation normalizes representations without modifying the semantic meaning of
    canonical payload data. Normalization is permitted; semantic transformation is not.

    The deterministic normalizer produces output solely from its declared inputs and
    has no observable side effects, external dependencies, hidden state, or environmental
    assumptions.
    """
    return CanonicalInterfacePayload(values=dict(representation.representation_values))
