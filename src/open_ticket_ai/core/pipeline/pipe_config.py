from __future__ import annotations

import enum
from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.registerable_config import RegisterableConfig


class FlowAction(enum.StrEnum):
    CONTINUE = "continue"
    FINISH_CONTAINER = "finish_container"
    FAIL_CONTAINER = "fail_container"


class RenderedPipeConfig(RegisterableConfig):
    model_config = ConfigDict(extra="allow")
    if_: bool = Field(default=True, alias="if")
    depends_on: list[str] = []

    @property
    def _if(self) -> bool:
        return self.if_


class RawPipeConfig(RegisterableConfig):
    model_config = ConfigDict(extra="allow")
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []

    @property
    def _if(self) -> str | bool:
        return self.if_


class PipeResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    success: bool
    failed: bool
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)

    def __and__(self, other: Self) -> Self:
        merged_data = {**self.data, **other.data}
        merged_msg = " ".join([m for m in [self.message, other.message] if m])
        return PipeResult(
            success=self.success and other.success,
            failed=self.failed and other.failed,
            message=merged_msg,
            data=merged_data,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        if not results:
            return PipeResult(success=True, failed=False)
        return reduce(lambda a, b: a & b, results)
