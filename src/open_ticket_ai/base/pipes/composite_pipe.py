from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class CompositePipe[ParamsT: BaseModel = StrictBaseModel](Pipe[ParamsT]):
    @staticmethod
    def get_params_model() -> type[StrictBaseModel]:
        return StrictBaseModel

    def __init__(self, factory: PipeFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._factory: PipeFactory = factory

    @final
    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        context = context.model_copy(update={"parent": context.params})
        return [await self._process_step(step_config, context) for step_config in self._config.steps or []]

    @final
    async def _process_step(self, step_config: PipeConfig, context: PipeContext) -> PipeResult:
        step_pipe = self._factory.render_pipe(step_config, context)
        return await step_pipe.process(context)

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.union(await self._process_steps(context))
