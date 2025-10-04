from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class Context(BaseModel):
    pipes: dict[str, PipeResult] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)

    def has_succeeded(self, pipe_id: str) -> bool:
        pipe_result = self.pipes.get(pipe_id)
        if pipe_result is None:
            return False
        return pipe_result.success and not pipe_result.failed
