from __future__ import annotations

import enum
from typing import Self, TypeVar

from pydantic import BaseModel, Field

from open_ticket_ai.core.config.raw_config import RawConfig


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"


ConfigModelType = TypeVar("ConfigModelType", bound=BaseModel)


class RenderedPipeConfig(BaseModel):
    name: str | None = None
    use: str
    services: dict[str, str] | None = None

    when: bool

    on_failure: OnType = OnType.FAIL_CONTAINER
    on_success: OnType = OnType.CONTINUE


class RawPipeConfig(RawConfig[RenderedPipeConfig]):
    name: str | None = None
    use: str
    services: dict[str, str] | None = None

    steps: list[Self] = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None
