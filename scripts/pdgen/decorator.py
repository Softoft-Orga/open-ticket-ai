from __future__ import annotations


def include_in_uml[T: type](cls: T) -> T:
    cls.__include_in_uml__ = True  # type: ignore[attr-defined]
    return cls
