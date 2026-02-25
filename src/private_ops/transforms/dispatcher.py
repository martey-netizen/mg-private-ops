from __future__ import annotations

from private_ops.protocol.models import (
    GraphPayload,
    RunMeta,
    TransformRequest,
    TransformResponse,
)
from private_ops.transforms.registry import get_transform, list_transforms


def dispatch(request: TransformRequest) -> TransformResponse:
    transform = get_transform(request.transform)
    if transform is None:
        run_meta = request.run_meta or RunMeta(
            run_id="unknown-run",
            transform=request.transform,
        )
        available = ', '.join(list_transforms()) or 'none'
        return TransformResponse(
            ok=False,
            status="error",
            graph=GraphPayload(run_meta=run_meta, nodes=[], edges=[]),
            errors=[f"Unknown transform '{request.transform}'. Available transforms: {available}."],
        )

    run_meta = request.run_meta
    if run_meta is None:
        request_id = "request"
        run_meta = RunMeta(
            run_id=f"run:{request.transform}:{request_id}",
            transform=request.transform,
            request_id=request_id,
        )

    graph = transform(TransformRequest(transform=request.transform, inputs=request.inputs, run_meta=run_meta))
    errors = graph.validate()
    return TransformResponse(
        ok=len(errors) == 0,
        status="ok" if not errors else "error",
        graph=graph,
        errors=errors,
    )
