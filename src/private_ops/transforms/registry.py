from __future__ import annotations

from collections.abc import Callable

from private_ops.adapters.maltego import to_maltego_mapping
from private_ops.protocol.models import (
    GraphPayload,
    RunMeta,
    TransformRequest,
    TransformResponse,
)

TransformFn = Callable[[TransformRequest], GraphPayload]
_REGISTRY: dict[str, TransformFn] = {}


def register(name: str) -> Callable[[TransformFn], TransformFn]:
    def _decorator(fn: TransformFn) -> TransformFn:
        _REGISTRY[name] = fn
        return fn

    return _decorator


def dispatch(request: TransformRequest) -> TransformResponse:
    transform = _REGISTRY.get(request.transform)
    if transform is None:
        run_meta = request.run_meta or RunMeta(
            run_id="unknown-run",
            transform=request.transform,
        )
        graph = GraphPayload(run_meta=run_meta, nodes=[], edges=[])
        return TransformResponse(
            ok=False,
            graph=graph,
            maltego={"entities": [], "links": []},
            errors=[f"unknown transform: {request.transform}"],
        )

    graph = transform(request)
    errors = graph.validate()
    return TransformResponse(
        ok=len(errors) == 0,
        graph=graph,
        maltego=to_maltego_mapping(graph),
        errors=errors,
    )
