from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class SimpleSequentialRunnerParams(BaseModel):
    on: PipeConfig = Field(..., description="trigger Pipe the run pipe only runs when this succeeds")
    run: PipeConfig = Field(..., description="Pipe to run when triggered")


class SimpleSequentialRunner(Pipe[SimpleSequentialRunnerParams]):
    def __init__(
        self, config: PipeConfig, logger_factory: LoggerFactory, pipe_factory: PipeFactory, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self._factory: PipeFactory = pipe_factory

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return SimpleSequentialRunnerParams

    async def _process(self, context: PipeContext) -> PipeResult:
        context = context.model_copy(update={"parent": context.params})
        self._logger.debug("RUNNNG SIMPLE SEQUENTIAL RUNNER")
        self._logger.debug(f"WITH PARAMS {self._params.model_dump()}")
        on_pipe = self._factory.create_pipe(self._params.on, context)
        self._logger.debug(f"ON PIPE {on_pipe}")
        run_pipe = self._factory.create_pipe(self._params.run, context)
        self._logger.debug(f"RUN PIPE {run_pipe}")

        on_pipe_result: PipeResult = await on_pipe.process(context)
        self._logger.debug(f"ON PIPE RESULT {on_pipe_result}")
        if on_pipe_result.has_succeeded():
            run_pipe_result: PipeResult = await run_pipe.process(context)
            return run_pipe_result
        return PipeResult.skipped(
            f"The On Pipe did not succeed: {on_pipe_result.message}, so the Run Pipe was not executed."
        )
