from __future__ import annotations

import hashlib


def _stable_hash(parts: tuple[str, ...]) -> str:
    hasher = hashlib.sha256()
    for part in parts:
        encoded = part.encode("utf-8")
        hasher.update(len(encoded).to_bytes(4, byteorder="big"))
        hasher.update(encoded)
    return hasher.hexdigest()[:24]


def node_id(entity_type: str, canonical_key: str) -> str:
    return f"n_{_stable_hash(('node', entity_type, canonical_key))}"


def edge_id(
    edge_type: str,
    from_node_id: str,
    to_node_id: str,
    canonical_key: str,
) -> str:
    return f"e_{_stable_hash(('edge', edge_type, from_node_id, to_node_id, canonical_key))}"
