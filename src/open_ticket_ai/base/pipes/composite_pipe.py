from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import CompositePipeResultData, PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


class CompositeParams(BaseModel):
    pass


class CompositePipeConfig(PipeConfig):
    steps: list[PipeConfig]


class CompositePipe(Pipe):
    """
    Composite pipe that runs multiple steps. Returns PipeResult from _process, Context from process.
    """

    def __init__(
        self,
        pipe_config: CompositePipeConfig,
        factory: RenderableFactory | None = None,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = CompositePipeConfig.model_validate(pipe_config.model_dump())
        # Validate params at runtime
        self.validated_params = CompositeParams.model_validate(self.params)
        self._factory = factory
        self._context: PipeContext | None = None

    def _build_pipe_from_step_config(self, step_config: PipeConfig, context: PipeContext) -> Pipe:
        """
        Build a child pipe from step config.
        Returns Pipe.
        """
        if self._factory is None:
            raise ValueError("RenderableFactory is required but not provided to CompositePipe")
        return self._factory.create_pipe(step_config, context)

    async def _process_steps(self, context: PipeContext) -> list[PipeResult[Any]]:
        """
        Run all steps and collect their PipeResults.
        Returns list[PipeResult].
        """
        results: list[PipeResult[Any]] = []
        current_context = context
        for step_pipe_config_raw in self.pipe_config.steps or []:
            current_context.parent = context
            step_pipe = self._build_pipe_from_step_config(step_pipe_config_raw, current_context)
            current_context = await step_pipe.process(current_context)
            if step_pipe_config_raw.id in current_context.pipes:
                results.append(current_context.pipes[step_pipe_config_raw.id])
        self._context = current_context
        return results

    async def _process(self) -> PipeResult[CompositePipeResultData]:
        raise NotImplementedError("CompositePipe must override process() to access context")

    async def process(self, context: PipeContext) -> PipeContext:
        self._logger.info(f"Processing pipe '{self.pipe_config.id}'")
        if self.pipe_config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info(f"Pipe '{self.pipe_config.id}' is running.")
            new_context = context.model_copy()
            try:
                steps_result: list[PipeResult[Any]] = await self._process_steps(new_context)
                composite_result = PipeResult.union(steps_result)
                if self._context:
                    new_context = self._context.model_copy()
            except Exception as e:
                self._logger.error(f"Error in pipe {self.pipe_config.id}: {str(e)}", exc_info=True)
                composite_result = PipeResult[CompositePipeResultData](
                    success=False, failed=True, message=str(e), data=CompositePipeResultData()
                )
            return self._save_pipe_result(new_context, composite_result)
        self._logger.info(f"Skipping pipe '{self.pipe_config.id}'.")
        return context
