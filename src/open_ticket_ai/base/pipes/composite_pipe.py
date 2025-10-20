from typing import Any, final

from pydantic import BaseModel, ConfigDict

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class CompositePipeParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")


class CompositePipe[ParamsT: BaseModel = CompositePipeParams](Pipe[ParamsT]):
    @staticmethod
    def get_params_model() -> type[CompositePipeParams]:
        return CompositePipeParams

    def __init__(self, pipe_factory: PipeFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._factory: PipeFactory = pipe_factory

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        context = context.model_copy(update={"parent": context.params})
        results = []
        for step_config in self._config.steps or []:
            result: PipeResult = await self._process_step(step_config, context)
            context = context.with_pipe_result(step_config.id, result)
            if result.has_failed():
                self._logger.warning(f"Step '{step_config.id}' failed. Skipping remaining steps in composite pipe.")
                break
            results.append(result)
        return results

    @final
    async def _process_step(
        self, step_config: PipeConfig, context: PipeContext, render_pipe: bool = True
    ) -> PipeResult:
        step_pipe = self._factory.create_pipe(step_config, context, render_pipe)
        return await step_pipe.process(context)

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.union(await self._process_steps(context))
