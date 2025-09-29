from __future__ import annotations

import enum
from typing import Self

from pydantic import Field

from open_ticket_ai.core.config.raw_config import RawRegisterableConfig, RenderableConfig, BaseRegisterableConfig, \
    RenderedRegistrableConfig


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"


class _BasePipeConfig(BaseRegisterableConfig):
    steps: list[Self] | str = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None


class RenderedPipeConfig(RenderedRegistrableConfig):
    steps: list[_BasePipeConfig] = Field(default_factory=list)
    when: bool

    on_failure: OnType = OnType.FAIL_CONTAINER
    on_success: OnType = OnType.CONTINUE


class RawPipeConfig(RawRegisterableConfig, _BasePipeConfig):
    pass


class PipeConfig(RenderableConfig[RawPipeConfig, RenderedPipeConfig]):
    pass
