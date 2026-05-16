"""Shared type alias for late-bound pipe parameters."""

from collections.abc import Callable

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext

type ContextResolver[T] = T | Callable[[PipeContext], T]


def resolve[T](value: ContextResolver[T], context: PipeContext) -> T:
    """Unwrap a ContextResolver: call it if callable, otherwise return as-is."""
    return value(context) if callable(value) else value
