from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class PipeContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    pipe_results: dict[str, PipeResult] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    parent: PipeContext | None = Field(default=None)

    def has_succeeded(self, pipe_id: str) -> bool:
        pipe_result = self.pipe_results.get(pipe_id)
        return pipe_result is not None and pipe_result.success

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result}
        return self.model_copy(update={"pipe_results": new_pipes})
