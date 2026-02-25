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


@register("resolve.phone_to_entities")
def resolve_phone_to_entities(request: TransformRequest) -> GraphPayload:
    raw_phone = str(request.inputs.get("phone", ""))
    normalized_phone = normalize_phone(raw_phone)

    run_meta = request.run_meta or RunMeta(
        run_id=f"run:{request.transform}:{normalized_phone}",
        transform=request.transform,
    )

    low_conf_source = SourceRef(
        source_id="starter-phone-transform",
        title="Deterministic placeholder entity generation",
        confidence=0.3,
    )

    phone_key = f"phone:{normalized_phone}"
    phone = Node(
        id=node_id("phone", phone_key),
        type="phone",
        canonical_key=phone_key,
        label=normalized_phone,
        properties={"raw": raw_phone, "normalized": normalized_phone, "confidence": 1.0},
        sources=[SourceRef(source_id="input", title="provided input", confidence=1.0)],
    )

    person_key = f"person:placeholder:{normalized_phone}"
    person = Node(
        id=node_id("person", person_key),
        type="person",
        canonical_key=person_key,
        label=f"Possible person owner {normalized_phone[-4:] if normalized_phone else 'unknown'}",
        properties={"placeholder": True, "confidence": 0.3},
        sources=[low_conf_source],
    )

    org_key = f"organization:placeholder:{normalized_phone}"
    org = Node(
        id=node_id("organization", org_key),
        type="organization",
        canonical_key=org_key,
        label=f"Possible organization owner {normalized_phone[-4:] if normalized_phone else 'unknown'}",
        properties={"placeholder": True, "confidence": 0.3},
        sources=[low_conf_source],
    )

    person_edge_key = f"associated_with:{phone_key}->{person_key}"
    org_edge_key = f"associated_with:{phone_key}->{org_key}"

    edges = [
        Edge(
            id=edge_id("associated_with", phone.id, person.id, person_edge_key),
            type="associated_with",
            from_id=phone.id,
            to_id=person.id,
            canonical_key=person_edge_key,
            properties={"confidence": 0.3},
            sources=[low_conf_source],
        ),
        Edge(
            id=edge_id("associated_with", phone.id, org.id, org_edge_key),
            type="associated_with",
            from_id=phone.id,
            to_id=org.id,
            canonical_key=org_edge_key,
            properties={"confidence": 0.3},
            sources=[low_conf_source],
        ),
    ]

    return GraphPayload(run_meta=run_meta, nodes=[phone, person, org], edges=edges)
