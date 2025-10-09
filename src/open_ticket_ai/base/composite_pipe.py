import logging
from typing import Any

from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult, RenderedPipeConfig, RawPipeConfig
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory


class CompositePipeConfig(RenderedPipeConfig):
    steps: list[RawPipeConfig]


class CompositePipe(Pipe):
    """
    Composite pipe that runs multiple steps. Returns PipeResult from _process, Context from process.
    """

    def __init__(self, config: CompositePipeConfig, factory: PipeFactory | None = None, *args, **kwargs) -> None:
        super().__init__(config, factory, *args, **kwargs)
        self.config = CompositePipeConfig.model_validate(config.model_dump())
        self._logger = logging.getLogger(self.__class__.__name__)
        self._factory = factory
        self._context: PipeContext | None = None

    def _build_pipe_from_step_config(self, step_config: RawPipeConfig, context: PipeContext) -> Pipe:
        """
        Build a child pipe from step config.
        Returns Pipe.
        """
        # Render the parent config before passing it to child pipes
        parent_config_rendered = self.config
        return self._factory.create_pipe(parent_config_rendered, step_config, context)

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        """
        Run all steps and collect their PipeResults.
        Returns list[PipeResult].
        """
        results: list[PipeResult] = []
        current_context = context
        for step_pipe_config_raw in self.config.steps:
            step_pipe = self._build_pipe_from_step_config(step_pipe_config_raw, current_context)
            current_context = await step_pipe.process(current_context)
            results.append(current_context.pipes[step_pipe_config_raw.id])
        # Update the context for parent to access
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
        self._logger.info("Processing pipe '%s'", self.config.id)
        if self.config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info("Pipe '%s' is running.", self.config.id)
            new_context = context.model_copy()
            try:
                steps_result: list[PipeResult] = await self._process_steps(new_context)
                composite_result = PipeResult.union(steps_result)
                # Update new_context with the latest state from step processing
                if self._context:
                    new_context = self._context.model_copy()
            except Exception as e:
                self._logger.error(f"Error in pipe {self.config.id}: {str(e)}", exc_info=True)
                composite_result = PipeResult(success=False, failed=True, message=str(e))
            return self._save_pipe_result(new_context, composite_result)
        self._logger.info("Skipping pipe '%s'.", self.config.id)
        return context
