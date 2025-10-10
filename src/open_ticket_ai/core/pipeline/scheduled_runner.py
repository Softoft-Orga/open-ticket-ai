from __future__ import annotations

import logging

from open_ticket_ai.core.pipeline.orchestrator_config import RunnerDefinition
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory


class ScheduledPipeRunner:
    def __init__(self, definition: RunnerDefinition, pipe_factory: PipeFactory) -> None:
        self.definition = definition
        self.pipe_factory = pipe_factory
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{definition.pipe_id}")

    async def execute(self) -> None:
        self._logger.info("Executing pipe '%s'", self.definition.pipe_id)
        try:
            pipe = self.pipe_factory.create_pipe(
                parent_config=None,
                pipe_config_raw=self.definition.pipe,
                scope=PipeContext(config=self.definition.pipe.model_dump()),
            )
            if pipe is None:
                self._logger.error("Failed to create pipe '%s'", self.definition.pipe_id)
                return
            if not isinstance(pipe, Pipe):
                self._logger.error("Created object is not a Pipe instance: %s", type(pipe))
                return

            context_result = await pipe.process(PipeContext())
            pipe_result = context_result.pipes.get(self.definition.pipe_id)

            if pipe_result and pipe_result.success:
                self._logger.info("Pipe '%s' completed successfully", self.definition.pipe_id)
            else:
                failure_message = pipe_result.message if pipe_result else "No result available"
                self._logger.warning(
                    "Pipe '%s' completed with failure: %s",
                    self.definition.pipe_id,
                    failure_message,
                )
        except Exception:
            self._logger.exception(
                "Pipe '%s' execution failed with exception",
                self.definition.pipe_id,
            )
