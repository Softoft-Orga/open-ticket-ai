import logging
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import CompositePipeResultData, PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


class CompositeParams(BaseModel):
    pass


class CompositePipeConfig(PipeConfig[CompositeParams]):
    steps: list[PipeConfig]


class CompositePipe(Pipe[CompositeParams]):
    """
    Composite pipe that runs multiple steps. Returns PipeResult from _process, Context from process.
    """

    def __init__(
        self, pipe_config: CompositePipeConfig, factory: RenderableFactory | None = None, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(pipe_config)
        self.pipe_config = pipe_config
        self._logger = logging.getLogger(self.__class__.__name__)
        self._factory = factory
        self._context: PipeContext | None = None

    def _build_pipe_from_step_config(self, step_config: PipeConfig, context: PipeContext) -> Pipe:
        """
        Build a child pipe from step config.
        Returns Pipe.
        """
        return self._factory.create_pipe(step_config, context)

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        """
        Run all steps and collect their PipeResults.
        Returns list[PipeResult].
        """
        results: list[PipeResult] = []
        current_context = context
        for step_pipe_config_raw in self.pipe_config.steps:
            current_context.parent = context
            step_pipe = self._build_pipe_from_step_config(step_pipe_config_raw, current_context)
            current_context = await step_pipe.process(current_context)
            results.append(current_context.pipes[step_pipe_config_raw.id])
        self._context = current_context
        return results

    async def _process(self) -> PipeResult:
        """
        Internal business logic. Runs all steps and returns aggregated PipeResult.
        Returns PipeResult.
        """
        # We need context to process steps, so we override process() to pass it
        raise NotImplementedError("CompositePipe must override process() to access context")

    async def process(self, context: PipeContext) -> PipeContext:
        """
        Public API. Runs composite pipe and returns updated Context.
        Overrides base implementation to access context during _process.
        """
        self._logger.info("Processing pipe '%s'", self.pipe_config.id)
        if self.pipe_config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info("Pipe '%s' is running.", self.pipe_config.id)
            new_context = context.model_copy()
            try:
                steps_result: list[PipeResult] = await self._process_steps(new_context)
                composite_result = PipeResult.union(steps_result)
                if self._context:
                    new_context = self._context.model_copy()
            except Exception as e:
                self._logger.error(f"Error in pipe {self.pipe_config.id}: {str(e)}", exc_info=True)
                composite_result = PipeResult[CompositePipeResultData](
                    success=False, failed=True, message=str(e), data=CompositePipeResultData()
                )
            return self._save_pipe_result(new_context, composite_result)
        self._logger.info("Skipping pipe '%s'.", self.pipe_config.id)
        return context
