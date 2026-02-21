from __future__ import annotations

import hashlib


def _stable_hash(parts: tuple[str, ...]) -> str:
    joined = "|".join(parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:24]


def node_id(entity_type: str, canonical_key: str) -> str:
    return f"n_{_stable_hash((entity_type, canonical_key))}"


def edge_id(
    edge_type: str,
    from_node_id: str,
    to_node_id: str,
    canonical_key: str,
) -> str:
    return f"e_{_stable_hash((edge_type, from_node_id, to_node_id, canonical_key))}"
