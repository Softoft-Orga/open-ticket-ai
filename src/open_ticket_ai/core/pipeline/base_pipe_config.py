from __future__ import annotations

import enum
from typing import Any, ClassVar, Self, TypeVar

from pydantic import BaseModel, Field

from open_ticket_ai.core.config.raw_config import RawConfig


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"




class _BasePipeConfig(BaseModel):
    name: str | None = None
    use: str
    services: dict[str, str] | str | None = None

    steps: list[Self] | str = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None


class RenderedPipeConfig(_BasePipeConfig):
    name: str = "anonymous"
    services: dict[str, str] | None = None
    steps: list[_BasePipeConfig] = Field(default_factory=list)
    when: bool

    on_failure: OnType = OnType.FAIL_CONTAINER
    on_success: OnType = OnType.CONTINUE


class RawPipeConfig(RawConfig[RenderedPipeConfig], _BasePipeConfig):
    rendered_model_type: ClassVar[type[RenderedPipeConfig]] = RenderedPipeConfig

    def _render_model_dump(self) -> dict[str, Any]:
        data = super().model_dump(exclude={"steps"})
        steps_value = self.steps

        if isinstance(steps_value, list):
            data["steps"] = list(steps_value)
        else:
            data["steps"] = steps_value

        return data

    def _post_render_transform(self, rendered: Any) -> Any:
        if isinstance(rendered, dict):
            return {
                key: value
                for key, value in rendered.items()
                if not (key in {"on_failure", "on_success"} and value is None)
            }

        return rendered
