"""Utility scripts for Open Ticket AI."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["ReadmeUpdater"]


def __getattr__(name: str) -> Any:
    if name == "ReadmeUpdater":
        return import_module("python_extras.scripts.readme_updater").ReadmeUpdater
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
