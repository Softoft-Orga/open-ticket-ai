from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.renderable import RenderableConfig

if TYPE_CHECKING:
    from typing import Any


class PipeConfig[ParamsT: BaseModel](RenderableConfig[ParamsT]):
    model_config = ConfigDict(populate_by_name=True)
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    steps: list[Any] | None = None

    @property
    def should_run(self) -> str | bool:
        return self.if_


class CompositePipeResultData(BaseModel):
    model_config = ConfigDict(extra="allow")


class PipeResult[DataT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    failed: bool
    message: str = ""
    data: DataT

    def __and__(self, other: Self) -> Self:
        merged_data_dict: dict = {**self.data.model_dump(), **other.data.model_dump()}
        merged_data = CompositePipeResultData.model_validate(merged_data_dict)
        merged_msg = ";\n ".join([m for m in [self.message, other.message] if m])
        return PipeResult[CompositePipeResultData](
            success=self.success and other.success,
            failed=self.failed and other.failed,
            message=merged_msg,
            data=merged_data,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult[DataT]]) -> PipeResult[CompositePipeResultData]:
        if not results:
            return PipeResult[CompositePipeResultData](success=True, failed=False, data=CompositePipeResultData())  # type: ignore
        return reduce(lambda a, b: a & b, results)
