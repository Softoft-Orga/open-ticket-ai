from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.renderable import RenderableConfig


class PipeConfig[ParamsT: BaseModel](RenderableConfig[ParamsT]):
    model_config = ConfigDict(extra="allow")
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    steps: list[PipeConfig[ParamsT]] | None = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        extra = self.model_extra or {}
        for k, v in extra.items():
            if k not in self.model_fields:
                self.params[k] = v
        self.model_extra = {}

    @property
    def should_run(self) -> str | bool:
        return self.if_


class PipeResult[DataT: BaseModel](BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    failed: bool
    message: str = ""
    data: DataT

    def __and__(self, other: Self) -> Self:
        merged_data_dict = {**self.data.model_dump(), **other.data.model_dump()}
        merged_data = type(self.data)(**merged_data_dict)
        merged_msg = " ".join([m for m in [self.message, other.message] if m])
        return PipeResult[DataT](
            success=self.success and other.success,
            failed=self.failed and other.failed,
            message=merged_msg,
            data=merged_data,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult[DataT]]) -> PipeResult[DataT]:
        if not results:
            return cls(success=True, failed=False, data=BaseModel())  # type: ignore
        return reduce(lambda a, b: a & b, results)
