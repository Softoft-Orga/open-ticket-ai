from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.renderable.renderable import RenderableConfig


class PipeConfig(RenderableConfig):
    model_config = ConfigDict(populate_by_name=True)
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    steps: list[Any] | None = None

    @property
    def should_run(self) -> str | bool:
        return self.if_


class PipeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool = True
    was_skipped: bool = False
    message: str = ""
    data: dict[str, Any] = {}

    def __and__(self, other: Self) -> PipeResult:
        merged_data_dict: dict[str, Any] = {**self.data, **other.data}
        merged_msg = ";\n ".join([m for m in [self.message, other.message] if m])
        return PipeResult(
            success=self.success and other.success,
            message=merged_msg,
            data=merged_data_dict,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        if not results:
            return PipeResult()
        return reduce(lambda a, b: a & b, results)

    @classmethod
    def empty(cls) -> PipeResult:
        return PipeResult()

    @classmethod
    def failure(cls, message: str) -> PipeResult:
        return PipeResult(success=False, message=message)

    @classmethod
    def skipped(cls, message: str = "") -> PipeResult:
        return PipeResult(was_skipped=True, message=message)
