from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class PipeContext(BaseModel):
    model_config = ConfigDict(ser_json_inf_nan="constants")

    pipes: dict[str, PipeResult[Any]] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    parent: PipeContext | None = Field(default=None, exclude=True)

    def has_succeeded(self, pipe_id: str) -> bool:
        pipe_result = self.pipes.get(pipe_id)
        if pipe_result is None:
            return False
        return pipe_result.success and not pipe_result.failed
