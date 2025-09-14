from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])


def inject(func: F) -> F:  # pragma: no cover - simple stub
    return func
