from __future__ import annotations

import json

import pytest
from pathlib import Path

from private_ops.adapters.maltego import to_maltego_mapping
from private_ops.cli import main
from private_ops.protocol.ids import edge_id, node_id
from private_ops.protocol.models import GraphPayload, RunMeta, TransformRequest
from private_ops.transforms import dispatch, get_transform, list_transforms, register


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


def test_id_hashing_is_unambiguous_for_delimiter_like_content() -> None:
    left = node_id("a", "b|c")
    right = node_id("a|b", "c")

    assert left != right


def test_registering_duplicate_transform_name_raises_error() -> None:
    from private_ops.transforms.registry import DuplicateTransformNameError

    @register("tests.duplicate_transform")
    def _first(request: TransformRequest) -> GraphPayload:
        return GraphPayload(
            run_meta=request.run_meta or RunMeta(run_id="r1", transform=request.transform),
            nodes=[],
            edges=[],
        )

    try:
        with pytest.raises(DuplicateTransformNameError):

            @register("tests.duplicate_transform")
            def _second(request: TransformRequest) -> GraphPayload:
                return GraphPayload(
                    run_meta=request.run_meta
                    or RunMeta(run_id="r2", transform=request.transform),
                    nodes=[],
                    edges=[],
                )
    finally:
        register("tests.duplicate_transform", override=True)(_first)


def test_dispatch_resolve_phone_to_entities_uses_phone_implementation() -> None:
    from private_ops.transforms import starter as _starter  # noqa: F401

    assert get_transform("starter.phone_to_entities") is not None

    request = TransformRequest(
        transform="resolve.phone_to_entities",
        inputs={"phone": "(555) 123-4567"},
    )
    response = dispatch(request)

    assert response.ok is True
    assert len(response.graph.nodes) == 3
    assert len(response.graph.edges) == 2


def test_registry_exposes_phone_transform() -> None:
    assert get_transform("resolve.phone_to_entities") is not None
    assert "resolve.phone_to_entities" in list_transforms()


def test_dispatch_unknown_transform_returns_error_status() -> None:
    response = dispatch(TransformRequest(transform="missing.transform", inputs={}))

    assert response.ok is False
    assert response.status == "error"
    assert "Unknown transform" in response.errors[0]


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


def test_phone_transform_is_deterministic_with_expected_graph_size() -> None:
    request = TransformRequest(
        transform="resolve.phone_to_entities",
        inputs={"phone": "(555) 123-4567"},
    )

    first = dispatch(request)
    second = dispatch(request)

    assert first.to_dict() == second.to_dict()
    assert first.ok is True
    assert first.status == "ok"
    assert len(first.graph.nodes) == 3
    assert len(first.graph.edges) == 2


def test_cli_run_transform_and_validate_graph_fixture(tmp_path: Path, monkeypatch) -> None:
    fixture_request = Path("tests/fixtures/phone_request.json")
    output_path = tmp_path / "out.json"
    ndjson_path = tmp_path / "out.ndjson"

    monkeypatch.setattr(
        "sys.argv",
        [
            "private_ops",
            "run-transform",
            str(fixture_request),
            "--out",
            str(output_path),
            "--ndjson",
            str(ndjson_path),
        ],
    )
    assert main() == 0

    response_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert response_payload["status"] == "ok"
    assert "maltego" in response_payload

    monkeypatch.setattr(
        "sys.argv",
        ["private_ops", "validate-graph", str(output_path)],
    )
    assert main() == 0
