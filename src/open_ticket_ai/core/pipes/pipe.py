import logging
from abc import ABC, abstractmethod
from typing import final

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class Pipe(ABC):
    def __init__(self, pipe_id: str = "") -> None:
        self._pipe_id = pipe_id or self.__class__.__name__
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{self._pipe_id}")

    @property
    def pipe_id(self) -> str:
        return self._pipe_id

    @final
    async def process(self, context: PipeContext) -> PipeResult:
        self._logger.info(f"Processing {self._pipe_id}")
        result: PipeResult = await self._process(context)
        self._logger.info(f"Processed {self._pipe_id}: {result.message or 'ok'}")
        return result

    @abstractmethod
    async def _process(self, context: PipeContext) -> PipeResult: ...
