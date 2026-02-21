from __future__ import annotations

from typing import Any

from private_ops.protocol.models import GraphPayload


def to_maltego_mapping(graph: GraphPayload) -> dict[str, Any]:
    entities: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []

    for node in graph.nodes:
        entities.append(
            {
                "id": node.id,
                "type": node.type,
                "value": node.label,
                "canonical_key": node.canonical_key,
                "properties": node.properties,
            }
        )

    for edge in graph.edges:
        links.append(
            {
                "id": edge.id,
                "type": edge.type,
                "from": edge.from_id,
                "to": edge.to_id,
                "canonical_key": edge.canonical_key,
                "properties": edge.properties,
            }
        )

    return {"entities": entities, "links": links}
