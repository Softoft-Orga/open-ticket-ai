from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.renderable.renderable import Renderable

from ..logging_iface import LoggerFactory
from .pipe_context import PipeContext
from .pipe_models import PipeConfig, PipeResult


class Pipe(Renderable, ABC):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())
        self._logger = logger_factory.create(self.__class__.__name__)

    async def process(self, context: PipeContext) -> PipeResult:
        if self._config.should_run and self._have_dependent_pipes_been_run(context):
            return await self._process()
        return PipeResult.skipped()

    def _have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self._config.depends_on)

    @abstractmethod
    async def _process(self) -> PipeResult:
        pass
