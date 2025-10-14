from typing import Any

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


class CompositePipeConfig(PipeConfig):
    steps: list[PipeConfig]


class CompositePipe(Pipe):
    def __init__(
        self,
        config: CompositePipeConfig,
        factory: RenderableFactory | None = None,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(config, logger_factory=logger_factory)
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        self.config = CompositePipeConfig.model_validate(config.model_dump())
        self._factory = factory

    def _build_pipe_from_step_config(self, step_config: PipeConfig, context: PipeContext) -> Pipe:
        if self._factory is None:
            raise ValueError("RenderableFactory is required but not provided to CompositePipe")
        return self._factory.create_pipe(step_config, context)

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        results: list[PipeResult] = []
        for step_config_raw in self.config.steps or []:
            context = context.model_copy(update={"parent": context.params})
            step_pipe = self._build_pipe_from_step_config(step_config_raw, context)
            context = await step_pipe.process(context)
            if step_config_raw.id in context.pipe_results:
                results.append(context.pipe_results[step_config_raw.id])
        return results

    async def _process_and_save(self, context: PipeContext) -> PipeContext:
        pipe_results = await self._process_steps(context)
        pipe_result = PipeResult.union(*pipe_results)
        return context.with_pipe_result(self.config.id, pipe_result)

    async def _process(self) -> PipeResult:
        raise NotImplementedError()
