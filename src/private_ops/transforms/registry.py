from __future__ import annotations

from collections.abc import Callable

from private_ops.protocol.models import GraphPayload, TransformRequest

TransformFn = Callable[[TransformRequest], GraphPayload]
_REGISTRY: dict[str, TransformFn] = {}


def register(name: str) -> Callable[[TransformFn], TransformFn]:
    def _decorator(fn: TransformFn) -> TransformFn:
        _REGISTRY[name] = fn
        return fn

    return _decorator


def get_transform(name: str) -> TransformFn | None:
    return _REGISTRY.get(name)


def list_transforms() -> list[str]:
    return sorted(_REGISTRY)
