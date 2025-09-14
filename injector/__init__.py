"""Minimal stub of the :mod:`injector` package used in tests.

Only the :func:`inject` decorator is implemented, acting as a no-op.
"""
from functools import wraps
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])


def inject(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper  # type: ignore[misc]
