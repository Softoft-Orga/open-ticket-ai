from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe_config import PipeResult

class Context(BaseModel):
    pipes: dict[str, PipeResult] = {}
    config: dict[str, Any] = {}
