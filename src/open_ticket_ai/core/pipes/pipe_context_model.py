from __future__ import annotations

from typing import Any

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class PipeContext(StrictBaseModel):
    pipe_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description=(
            "Dictionary mapping pipe IDs to their execution results "
            "for accessing outputs from previously executed pipes."
        ),
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Dictionary of parameters available to all pipes in the execution context "
            "for sharing configuration and data."
        ),
    )
    parent: PipeContext | None = Field(
        default=None,
        description=(
            "Optional reference to the parent context for nested pipes execution "
            "allowing access to outer scope results."
        ),
    )

    def has_succeeded(self, pipe_id: str) -> bool:
        if pipe_id not in self.pipe_results:
            return False
        pipe_result = PipeResult.model_validate(self.pipe_results[pipe_id])
        return pipe_result.succeeded and not pipe_result.was_skipped

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result}
        return self.model_copy(update={"pipe_results": new_pipes})

    def with_model(self, pipe_result: PipeResult) -> PipeContext:
        return self.model_copy(update={"params": {**self.params, **pipe_result.data}})
