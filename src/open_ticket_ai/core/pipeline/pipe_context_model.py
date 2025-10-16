from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, Field

from open_ticket_ai.core.base_model import OpenTicketAIBaseModel
from open_ticket_ai.core.pipeline.pipe_models import PipeResult


class PipeContext(OpenTicketAIBaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pipe_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description=(
            "Dictionary mapping pipe IDs to their execution results "
            "for accessing outputs from previously executed pipes."
        )
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Dictionary of parameters available to all pipes in the execution context "
            "for sharing configuration and data."
        )
    )
    parent: PipeContext | None = Field(
        default=None,
        description=(
            "Optional reference to the parent context for nested pipeline execution "
            "allowing access to outer scope results."
        )
    )

    def has_succeeded(self, pipe_id: str) -> bool:
        if pipe_id not in self.pipe_results:
            return False
        pipe_result = PipeResult.model_validate(self.pipe_results[pipe_id])
        return pipe_result.succeeded and not pipe_result.was_skipped

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result}
        return self.model_copy(update={"pipe_results": new_pipes})
