from __future__ import annotations

import enum
from typing import Any

from pydantic import Field

from open_ticket_ai.core.config.registerable_config import RegisterableConfig


class OnType(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"


class RenderedPipeConfig(RegisterableConfig):
    steps: list[dict[str, Any]] = Field(default_factory=list)
    when: bool

    on_failure: OnType = OnType.FAIL_CONTAINER
    on_success: OnType = OnType.CONTINUE


class RawPipeConfig(RegisterableConfig):
    steps: list[dict[str, Any]] = Field(default_factory=list)

    when: str = "True"

    on_failure: str | None = None
    on_success: str | None = None

