from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BasePipeConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    use: str = "Default"  # Default is JinjaExpressionPipe
    config: dict[str, Any] = Field(default_factory=dict)
    when: str = "True"

    # Optional execution flow controls and service bindings
    on_failure: str | None = None
    on_success: str | None = None
    services: dict[str, str] | None = None

    # Scratchpad and nested steps
    data: dict[str, Any] = Field(default_factory=dict)
    steps: list["BasePipeConfig"] = Field(default_factory=list)
