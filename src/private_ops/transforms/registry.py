from __future__ import annotations

from collections.abc import Callable

from private_ops.protocol.models import GraphPayload, TransformRequest

TransformFn = Callable[[TransformRequest], GraphPayload]
_REGISTRY: dict[str, TransformFn] = {}


class DuplicateTransformNameError(ValueError):
    """Raised when attempting to register a transform name that already exists."""


def register(name: str, *, override: bool = False) -> Callable[[TransformFn], TransformFn]:
    def _decorator(fn: TransformFn) -> TransformFn:
        if name in _REGISTRY and not override:
            raise DuplicateTransformNameError(
                f"Transform '{name}' is already registered. "
                "Pass override=True to replace it explicitly."
            )
        _REGISTRY[name] = fn
        return fn

    return _decorator


def get_transform(name: str) -> TransformFn | None:
    return _REGISTRY.get(name)


def list_transforms() -> list[str]:
    return sorted(_REGISTRY)
