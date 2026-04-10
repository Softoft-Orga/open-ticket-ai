from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel


class PipeResult(StrictBaseModel):
    succeeded: bool = Field(default=True)
    was_skipped: bool = Field(default=False)
    message: str = Field(default="")
    data: dict[str, Any] = Field(default_factory=dict)

    def __and__(self, other: Self) -> PipeResult:
        return PipeResult.model_construct(
            succeeded=self.succeeded and other.succeeded,
            was_skipped=self.was_skipped and other.was_skipped,
            message=(f"{self.message}; {other.message}".strip("; ")),
            data={**self.data, **other.data},
        )

    def has_succeeded(self) -> bool:
        return self.succeeded

    def has_failed(self) -> bool:
        return not self.succeeded and not self.was_skipped

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        return reduce(lambda a, b: a & b, results, PipeResult.empty())

    @classmethod
    def empty(cls) -> PipeResult:
        return PipeResult.model_validate({})

    @classmethod
    def failure(cls, message: str) -> PipeResult:
        return PipeResult.model_validate({"succeeded": False, "message": message})

    @classmethod
    def skipped(cls, message: str = "") -> PipeResult:
        return PipeResult.model_validate({"succeeded": False, "was_skipped": True, "message": message})

    @classmethod
    def success(cls, message: str = "", data: dict[str, Any] | None = None) -> PipeResult:
        return PipeResult.model_validate({"message": message, "data": data or {}})
