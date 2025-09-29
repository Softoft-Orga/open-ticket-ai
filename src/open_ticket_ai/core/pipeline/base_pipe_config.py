from __future__ import annotations

import enum
from typing import Self, TypeVar

from pydantic import BaseModel, Field

from open_ticket_ai.core.config.raw_config import RawConfig


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"




class _BasePipeConfig(BaseModel):
    name: str | None = None
    use: str | None = None
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
    pass