from __future__ import annotations

import enum
from typing import Self

from pydantic import Field

from open_ticket_ai.core.config.raw_config import RenderableConfig
from open_ticket_ai.core.config.registerable import RawRegisterableConfig, RenderedRegistrableConfig
from open_ticket_ai.core.pipeline.base_pipe import BasePipe


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"


class _BasePipeConfig(RawRegisterableConfig):
    steps: list[Self] | str = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None


class RenderedPipeConfig(RenderedRegistrableConfig):
    steps: list[BasePipe[RawPipeConfig, Self]] = Field(default_factory=list)
    when: bool

    on_failure: OnType = OnType.FAIL_CONTAINER
    on_success: OnType = OnType.CONTINUE


class RawPipeConfig(RawRegisterableConfig):
    steps: list[Self] | str = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None


class PipeConfig(RenderableConfig[RawPipeConfig, RenderedPipeConfig]):
    pass
