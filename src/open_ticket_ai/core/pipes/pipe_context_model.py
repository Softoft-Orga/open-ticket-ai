from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core._util.hashes import freeze
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class PipeContext(StrictBaseModel):
    pipe_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description=(
            "Dictionary mapping pipe IDs to their execution results "
            "for accessing outputs from previously executed pipes."
        ),
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Dictionary of parameters available to all pipes in the execution context "
            "for sharing configuration and data."
        ),
    )
    parent_params: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Optional reference to the parent context for nested pipes execution "
            "allowing access to outer scope results."
        ),
    )

    def _key(self) -> tuple[Any, ...]:
        return freeze(self.pipe_results), freeze(self.params), freeze(self.parent_params)

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PipeContext):
            return False
        return hash(self) == hash(other)

    def has_succeeded(self, pipe_id: str) -> bool:
        if pipe_id not in self.pipe_results:
            return False
        pipe_result = PipeResult.model_validate(self.pipe_results[pipe_id])
        return pipe_result.succeeded and not pipe_result.was_skipped

    def with_pipe_result(self, pipe_id: str, pipe_result: PipeResult) -> PipeContext:
        new_pipes = {**self.pipe_results, pipe_id: pipe_result.model_dump()}
        return self.model_copy(update={"pipe_results": new_pipes})

    def with_parent(self, parent_params: BaseModel) -> PipeContext:
        return self.model_copy(update={"parent_params": parent_params.model_dump()})

    @property
    def parent(self) -> dict[str, Any] | None:
        return self.parent_params

    @staticmethod
    def empty() -> PipeContext:
        return PipeContext()
