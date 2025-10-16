from __future__ import annotations

from abc import ABC
from typing import Any, final

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.renderable.renderable import Renderable


class Pipe[ParamsT: StrictBaseModel](Renderable[ParamsT], ABC):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())
        self._logger = logger_factory.create(self.__class__.__name__)

    @final
    async def process(self, context: PipeContext) -> PipeResult:
        if self._config.should_run and self._are_dependencies_fulfilled(context):
            return await self._process(context)
        return PipeResult.skipped()

    @final
    def _are_dependencies_fulfilled(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(pipe_id) for pipe_id in self._config.depends_on)

    async def _process(self, *args: Any, **kwargs: Any) -> PipeResult:
        return PipeResult.skipped()
