from typing import Any

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


class CompositePipe(Pipe):
    @staticmethod
    def get_params_model() -> type[Any]:
        return PipeConfig

    def __init__(
        self,
        factory: RenderableFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._factory = factory

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        context = context.model_copy(update={"parent": context.params})
        return [await self.process_step(step_config, context) for step_config in self._config.steps]

    async def process_step(self, step_config: PipeConfig, context: PipeContext) -> PipeResult:
        step_pipe = self._factory.render(step_config, context)
        return await step_pipe.process(context)

    async def _process_and_save(self, context: PipeContext) -> PipeContext:
        pipe_results = await self._process_steps(context)
        pipe_result = PipeResult.union(*pipe_results)
        return context.with_pipe_result(self._config.id, pipe_result)

    async def _process(self) -> PipeResult:
        raise NotImplementedError()
