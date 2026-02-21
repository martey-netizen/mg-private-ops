from __future__ import annotations

from private_ops.adapters.maltego import to_maltego_mapping
from private_ops.protocol.ids import edge_id, node_id
from private_ops.protocol.models import GraphPayload, RunMeta, TransformRequest
from private_ops.transforms import dispatch


def test_graph_model_validation_detects_bad_edges() -> None:
    graph = GraphPayload.from_dict(
        {
            "run_meta": {"run_id": "r1", "transform": "t1"},
            "nodes": [
                {
                    "id": "n1",
                    "type": "phone",
                    "canonical_key": "phone:+15551234567",
                    "label": "+15551234567",
                }
            ],
            "edges": [
                {
                    "id": "e1",
                    "type": "ownership",
                    "from": "n1",
                    "to": "missing",
                    "canonical_key": "k1",
                }
            ],
        }
    )

    errors = graph.validate()
    assert any("unknown to node" in err for err in errors)


def test_ids_are_stable() -> None:
    n1 = node_id("phone", "phone:+15551234567")
    n2 = node_id("phone", "phone:+15551234567")
    e1 = edge_id("ownership", n1, "n-target", "k")
    e2 = edge_id("ownership", n1, "n-target", "k")

    assert n1 == n2
    assert e1 == e2


def test_adapter_output_shape() -> None:
    request = TransformRequest(
        transform="resolve.phone_to_entities",
        inputs={"phone": "+1 (555) 123-4567"},
        run_meta=RunMeta(run_id="run-1", transform="resolve.phone_to_entities"),
    )
    response = dispatch(request)

    mapping = to_maltego_mapping(response.graph)
    assert isinstance(mapping["entities"], list)
    assert isinstance(mapping["links"], list)
    assert {"id", "type", "value"}.issubset(mapping["entities"][0].keys())


def test_starter_transform_is_deterministic() -> None:
    request = TransformRequest(
        transform="resolve.phone_to_entities",
        inputs={"phone": "(555) 123-4567"},
    )

    first = dispatch(request)
    second = dispatch(request)

    assert first.to_dict() == second.to_dict()
    assert first.ok is True
