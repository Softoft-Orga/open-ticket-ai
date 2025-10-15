from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.pipeline.pipe_models import PipeResult


class PipeContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    pipe_results: dict[str, dict[str, Any]] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    parent: PipeContext | None = Field(default=None)

    def has_succeeded(self, pipe_id: str) -> bool:
        if pipe_id not in self.pipe_results:
            return False
        pipe_result = PipeResult.model_validate(self.pipe_results[pipe_id])
        return pipe_result.succeeded and not pipe_result.was_skipped

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result}
        return self.model_copy(update={"pipe_results": new_pipes})
