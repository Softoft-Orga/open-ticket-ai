from typing import Any

from pydantic import BaseModel


class PipelineContext(BaseModel):
    pipes: dict[str, dict[str, Any]] = {}
    config: dict[str, Any] = {}
