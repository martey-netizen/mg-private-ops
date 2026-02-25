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

    graph = transform(request)
    errors = graph.validate()
    return TransformResponse(
        ok=len(errors) == 0,
        status="ok" if not errors else "error",
        graph=graph,
        errors=errors,
    )
