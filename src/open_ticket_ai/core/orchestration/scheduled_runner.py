from __future__ import annotations

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_config import RunnerDefinition
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


class PipeRunner:
    def __init__(
        self, definition: RunnerDefinition, pipe_factory: RenderableFactory, logger_factory: LoggerFactory
    ) -> None:
        self.definition = definition
        self.pipe_factory = pipe_factory
        self._logger = logger_factory.get_logger(f"{self.__class__.__name__}.{definition.pipe_id}")

    async def on_trigger_fired(self) -> None:
        await self.execute()

    async def execute(self) -> None:
        self._logger.info(f"Executing pipe '{self.definition.pipe_id}'")
        context = PipeContext(params=self.definition.run.params)
        pipe = self.pipe_factory.render(
            config_raw=self.definition.run,
            scope=context,
        )
        if pipe is None:
            self._logger.error(f"Failed to create pipe '{self.definition.pipe_id}'")
            return
        if not isinstance(pipe, Pipe):
            self._logger.error(f"Created object is not a Pipe instance: {type(pipe)}")
            return

        context_result = await pipe.process(context)
        pipe_result = context_result.pipe_results.get(self.definition.pipe_id)

        if pipe_result and pipe_result.success:
            self._logger.info(f"Pipe '{self.definition.pipe_id}' completed successfully")
        else:
            failure_message = pipe_result.message if pipe_result else "No result available"
            self._logger.warning(f"Pipe '{self.definition.pipe_id}' completed with failure: {failure_message}")
