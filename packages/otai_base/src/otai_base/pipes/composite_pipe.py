from typing import Annotated, Any, ClassVar, final

from open_ticket_ai import NoRenderField, Pipe, PipeFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from pydantic import BaseModel, ConfigDict


class CompositePipeParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    steps: Annotated[
        list[PipeConfig],
        NoRenderField(
            default_factory=list,
            description="List of pipe configurations representing the steps in the composite pipe.",
        ),
    ]


class CompositePipe[ParamsT: CompositePipeParams = CompositePipeParams](Pipe[ParamsT]):
    ParamsModel: ClassVar[type[CompositePipeParams]] = CompositePipeParams

    def __init__(self, pipe_factory: PipeFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._factory: PipeFactory = pipe_factory

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        context = context.with_parent(self._params)
        results = []
        for step_config in self._params.steps or []:
            result: PipeResult = await self._process_step(step_config, context)
            context = context.with_pipe_result(step_config.id, result)
            if result.has_failed():
                self._logger.warning(f"Step '{step_config.id}' failed. Skipping remaining steps in composite pipe.")
                break
            results.append(result)
        return results

    @final
    async def _process_step(self, step_config: PipeConfig, context: PipeContext) -> PipeResult:
        step_pipe = await self._factory.create_pipe(step_config, context)
        return await step_pipe.process(context)

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.union(await self._process_steps(context))
