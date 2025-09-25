from typing import Any

from pydantic import BaseModel, Field


class BasePipeConfig(BaseModel):
    class_path: str = Field(..., description="Dotted path to the Pipe class")
    when: str = "true"
    output: dict[str, Any] = Field(
        default_factory=dict,
        description="Templated output mapping to inject into the pipeline context",
    )
