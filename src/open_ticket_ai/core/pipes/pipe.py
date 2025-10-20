from __future__ import annotations

from abc import ABC
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class Pipe[ParamsT: BaseModel](Injectable[ParamsT], ABC):
    cacheable = False

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._logger.debug(f"Initializing pipe: {self.__class__.__name__} with config: {config.model_dump()}")
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())

    @final
    async def process(self, context: PipeContext) -> PipeResult:
        if await self._should_run(context):
            return await self._process(context)
        return PipeResult.skipped()

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        return PipeResult.skipped()

    async def _should_run(self, _: PipeContext) -> bool:
        return self._config.should_run
