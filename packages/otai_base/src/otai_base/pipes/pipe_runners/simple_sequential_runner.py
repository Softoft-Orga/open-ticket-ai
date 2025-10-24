from typing import Annotated, Any, ClassVar

from open_ticket_ai import LoggerFactory, NoRenderField, Pipe, PipeFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from pydantic import BaseModel


class SimpleSequentialRunnerParams(BaseModel):
    on: Annotated[PipeConfig, NoRenderField(description="Trigger pipe that gates execution")]
    run: Annotated[PipeConfig, NoRenderField(description="Pipe to run when triggered")]


class SimpleSequentialRunner(Pipe[SimpleSequentialRunnerParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleSequentialRunnerParams

    def __init__(
        self, config: PipeConfig, logger_factory: LoggerFactory, pipe_factory: PipeFactory, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._factory: PipeFactory = pipe_factory

    async def _process(self, context: PipeContext) -> PipeResult:
        context = context.model_copy(update={"parent": context.params})
        on_pipe = await self._factory.create_pipe(self._params.on, context)
        run_pipe = await self._factory.create_pipe(self._params.run, context)

        on_pipe_result: PipeResult = await on_pipe.process(context)
        if on_pipe_result.has_succeeded():
            run_pipe_result: PipeResult = await run_pipe.process(context)
            return run_pipe_result
        return PipeResult.skipped(
            f"The On Pipe did not succeed: {on_pipe_result.message}, so the Run Pipe was not executed."
        )
