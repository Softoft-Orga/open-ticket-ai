import asyncio
import logging
from typing import Any, Dict

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.base_pipe_config import BasePipeConfig


class Orchestrator:
    def __init__(self, pipe_config: BasePipeConfig, interval_seconds: float = 60.0):
        self.pipe_config = pipe_config
        self.interval_seconds = interval_seconds
        self._logger = logging.getLogger(__name__)
        self._pipe = Pipe(pipe_config)

    async def run(self, initial_context: Dict[str, Any] = None) -> None:
        self._logger.info(f"Starting orchestrator with interval: {self.interval_seconds}s")
        
        context = PipelineContext()
        if initial_context:
            context.config.update(initial_context)

        while True:
            try:
                context = await self._pipe.process(context)
                self._logger.debug("Pipe execution completed successfully")
                await asyncio.sleep(self.interval_seconds)
                
            except Exception as e:
                self._logger.error(f"Error in pipe execution: {e}", exc_info=True)
                raise
