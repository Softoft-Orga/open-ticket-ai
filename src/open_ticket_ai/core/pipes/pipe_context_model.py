from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core._util.hashes import freeze
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class PipeContext(StrictBaseModel):
    pipe_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Mapping of pipe IDs to their serialised PipeResult dicts.",
    )

    def _key(self) -> tuple[Any, ...]:
        return (freeze(self.pipe_results),)

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PipeContext):
            return False
        return hash(self) == hash(other)

    def get_result(self, pipe_id: str, data_key: str = "value") -> Any:
        """Retrieve a data value from a previously executed pipe's result."""
        if pipe_id not in self.pipe_results:
            available = list(self.pipe_results.keys())
            raise KeyError(f"Pipe '{pipe_id}' not found in context. Available: {available}")
        data = self.pipe_results[pipe_id].get("data", {})
        if data_key not in data:
            available = list(data.keys())
            raise KeyError(
                f"Data key '{data_key}' not found in pipe '{pipe_id}' result. Available: {available}"
            )
        return data[data_key]

    def has_succeeded(self, pipe_id: str) -> bool:
        if pipe_id not in self.pipe_results:
            return False
        pipe_result = PipeResult.model_validate(self.pipe_results[pipe_id])
        return pipe_result.succeeded and not pipe_result.was_skipped

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result.model_dump()}
        return self.model_copy(update={"pipe_results": new_pipes})

    @staticmethod
    def empty() -> PipeContext:
        return PipeContext()
