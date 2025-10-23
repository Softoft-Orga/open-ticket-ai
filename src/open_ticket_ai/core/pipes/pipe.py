from abc import ABC
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class Pipe[ParamsT: BaseModel = StrictBaseModel](Injectable[ParamsT], ABC):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())

    @final
    async def process(self, context: PipeContext) -> PipeResult:
        return await self._process(context)

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        return PipeResult.skipped()
