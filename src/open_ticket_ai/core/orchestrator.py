import asyncio
import logging
from typing import Any

from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.base_pipe import BasePipe


class Orchestrator:
    def __init__(self, pipes: list[BasePipe], interval_seconds: float = 60.0):
        """Initialize Orchestrator with injected Pipe instances.

        Args:
            pipes: List of configured Pipe instances to orchestrate
            interval_seconds: Interval between pipeline executions
        """
        self.pipes = pipes
        self.interval_seconds = interval_seconds
        self._logger = logging.getLogger(__name__)

        if not pipes:
            raise ValueError("At least one pipe must be provided to the Orchestrator")

    async def run(self, initial_context: dict[str, Any] = None) -> None:
        self._logger.info(f"Starting orchestrator with {len(self.pipes)} pipes, interval: {self.interval_seconds}s")

        context = PipelineContext()
        if initial_context:
            context.config.update(initial_context)

        while True:
            try:
                # Execute all pipes in sequence
                for i, pipe in enumerate(self.pipes):
                    self._logger.debug(f"Executing pipe {i + 1}/{len(self.pipes)}: {pipe.__class__.__name__}")
                    context = await pipe.process(context)

                self._logger.debug("All pipes executed successfully")
                await asyncio.sleep(self.interval_seconds)

            except Exception as e:
                self._logger.error(f"Error in pipe execution: {e}", exc_info=True)
                raise
