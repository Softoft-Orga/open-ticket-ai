from typing import Any
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BasePipeConfig(BaseModel):
    model_config = ConfigDict(extra='allow')

    name: Optional[str] = None
    use: str = "Default"  # Default is JinjaExpressionPipe
    config: dict[str, Any] = Field(default_factory=dict)
    when: str = "True"

    # Optional execution flow controls and service bindings
    on_failure: Optional[str] = None
    on_success: Optional[str] = None
    services: Optional[dict[str, str]] = None

    # Scratchpad and nested steps
    data: dict[str, Any] = Field(default_factory=dict)
    steps: list['BasePipeConfig'] = Field(default_factory=list)
