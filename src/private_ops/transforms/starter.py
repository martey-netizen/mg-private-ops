from __future__ import annotations

from private_ops.protocol.ids import edge_id, node_id
from private_ops.protocol.models import (
    Edge,
    GraphPayload,
    Node,
    RunMeta,
    SourceRef,
    TransformRequest,
)
from private_ops.protocol.normalize import normalize_phone
from private_ops.transforms.registry import register


@register("starter.phone_to_entities")
def resolve_phone_to_entities(request: TransformRequest) -> GraphPayload:
    raw_phone = str(request.inputs.get("phone", ""))
    normalized_phone = normalize_phone(raw_phone)

    run_meta = request.run_meta or RunMeta(
        run_id=f"run:resolve.phone_to_entities:{normalized_phone}",
        transform=request.transform,
    )

    source = SourceRef(
        source_id="starter-transform",
        title="Deterministic starter transform",
        confidence=0.5,
    )

    phone_canonical = f"phone:{normalized_phone}"
    phone_node = Node(
        id=node_id("phone", phone_canonical),
        type="phone",
        canonical_key=phone_canonical,
        label=normalized_phone,
        properties={"raw": raw_phone, "normalized": normalized_phone},
        sources=[source],
    )

    person_canonical = f"person:subscriber:{normalized_phone}"
    person_node = Node(
        id=node_id("person", person_canonical),
        type="person",
        canonical_key=person_canonical,
        label=f"Subscriber {normalized_phone[-4:] if normalized_phone else 'unknown'}",
        properties={"role": "subscriber"},
        sources=[source],
    )

    relation_key = f"owns:{phone_canonical}->{person_canonical}"
    phone_edge = Edge(
        id=edge_id("ownership", phone_node.id, person_node.id, relation_key),
        type="ownership",
        from_id=phone_node.id,
        to_id=person_node.id,
        canonical_key=relation_key,
        properties={"asserted_by": "starter_transform"},
        sources=[source],
    )

    return GraphPayload(run_meta=run_meta, nodes=[phone_node, person_node], edges=[phone_edge])
