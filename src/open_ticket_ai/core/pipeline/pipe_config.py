from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.renderable.renderable import RenderableConfig, EmptyModel


class PipeConfig(RenderableConfig):
    model_config = ConfigDict(populate_by_name=True)
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    steps: list[Any] | None = None

    @property
    def should_run(self) -> str | bool:
        return self.if_


class CompositePipeResultData(BaseModel):
    model_config = ConfigDict(extra="allow")


class PipeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    message: str = ""
    data: BaseModel = Field(default_factory=EmptyModel)

    def __and__(self, other: Self) -> PipeResult:
        merged_data_dict: dict[str, Any] = {**self.data.model_dump(), **other.data.model_dump()}
        merged_data = CompositePipeResultData.model_validate(merged_data_dict)
        merged_msg = ";\n ".join([m for m in [self.message, other.message] if m])
        return PipeResult(
            success=self.success and other.success,
            message=merged_msg,
            data=merged_data,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        if not results:
            return PipeResult(success=True, data=CompositePipeResultData())
        return reduce(lambda a, b: a & b, results)
