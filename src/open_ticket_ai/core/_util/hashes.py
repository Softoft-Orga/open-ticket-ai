from typing import Any


def freeze(v: Any) -> Any:
    if isinstance(v, dict):
        return tuple(sorted((k, freeze(x)) for k, x in v.items()))
    if isinstance(v, list):
        return tuple(freeze(x) for x in v)
    if isinstance(v, set):
        return tuple(sorted(freeze(x) for x in v))
    return v
