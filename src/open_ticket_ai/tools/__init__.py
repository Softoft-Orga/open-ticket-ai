"""Utility helpers for working with OpenTicketAI configuration files."""

from __future__ import annotations

from typing import Any

__all__ = ["generate_mermaid_diagram"]


def __getattr__(name: str) -> Any:
    if name == "generate_mermaid_diagram":
        from .config_to_mermaid import generate_mermaid_diagram

        return generate_mermaid_diagram
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
