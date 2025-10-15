from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import ConfigDict, Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class PipeConfig(RenderableConfig):
    model_config = ConfigDict(populate_by_name=True)
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    steps: list[PipeConfig] | None = None

    @property
    def should_run(self) -> str | bool:
        return self.if_


class PipeResult(StrictBaseModel):
    succeeded: bool = True
    was_skipped: bool = False
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)

    def __and__(self, other: Self) -> PipeResult:
        return PipeResult(
            succeeded=self.succeeded and other.succeeded,
            was_skipped=self.was_skipped and other.was_skipped,
            message=(f"{self.message}; {other.message}".strip("; ")),
            data={**self.data, **other.data},
        )

    def has_failed(self) -> bool:
        return not self.succeeded and not self.was_skipped

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        return reduce(lambda a, b: a & b, results)

    @classmethod
    def empty(cls) -> PipeResult:
        return PipeResult()

    @classmethod
    def failure(cls, message: str) -> PipeResult:
        return PipeResult(succeeded=False, message=message)

    @classmethod
    def skipped(cls, message: str = "") -> PipeResult:
        return PipeResult(was_skipped=True, message=message)

    @classmethod
    def success(cls, message: str = "", data: dict[str, Any] = None) -> PipeResult:
        return PipeResult(message=message, data=data or {})
