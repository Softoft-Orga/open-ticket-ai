from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict

from open_ticket_ai.core.renderable.renderable import Renderable

from ..logging_iface import LoggerFactory
from .pipe_config import PipeConfig, PipeResult
from .pipe_context import PipeContext


class ParamsModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class Pipe(Renderable, ABC):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._config = PipeConfig.model_validate(config.model_dump())
        self._logger = logger_factory.get_logger(self.__class__.__name__)

    def _have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self._config.depends_on)

    async def process(self, context: PipeContext) -> PipeContext:
        self._logger.info(f"Processing pipe '{self._config.id}'")
        if self._config.should_run and self._have_dependent_pipes_been_run(context):
            self._logger.info(f"Pipe '{self._config.id}' is running.")

            return await self._process_and_save(context)
        self._logger.info(f"Skipping pipe '{self._config.id}'.")
        return context

    async def _process_and_save(self, context: PipeContext) -> PipeContext:
        pipe_result = await self._process()
        return context.with_pipe_result(self._config.id, pipe_result)

    @abstractmethod
    async def _process(self) -> PipeResult:
        pass
