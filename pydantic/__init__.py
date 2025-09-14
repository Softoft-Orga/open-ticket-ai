"""Very small stub of the :mod:`pydantic` package used for unit tests.

The implementation is intentionally tiny and only supports the features used in
our tests: a :class:`BaseModel` with a ``model_dump`` method, a ``Field`` helper
returning default values and a ``model_validator`` decorator acting as a no-op.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, TypeVar


class BaseModel:
    def __init__(self, **data: Any):
        # populate defaults defined on the class
        for name, value in self.__class__.__dict__.items():
            if not name.startswith("_") and not callable(value):
                setattr(self, name, value)
        # override with provided data
        for key, value in data.items():
            setattr(self, key, value)

    def model_dump(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if isinstance(value, BaseModel):
                result[key] = value.model_dump()
            elif isinstance(value, list):
                result[key] = [v.model_dump() if isinstance(v, BaseModel) else v for v in value]
            else:
                result[key] = value
        return result


def Field(default: Any = None, **_: Any) -> Any:  # pragma: no cover - behaviourless helper
    return default


F = TypeVar("F", bound=Callable[..., Any])


def model_validator(*_args: Any, **_kwargs: Any):  # pragma: no cover - acts as identity decorator
    def decorator(func: F) -> F:
        return func

    return decorator
