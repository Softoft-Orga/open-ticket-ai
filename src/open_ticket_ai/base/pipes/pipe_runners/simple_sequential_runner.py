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
        self._logger.info(f"🎯 Runner {self._config.id}: Checking trigger condition")
        self._logger.debug(f"Trigger pipe: {self._params.on.id}, Run pipe: {self._params.run.id}")

        context = context.model_copy(update={"parent": context.params})
        on_pipe = self._factory.render_pipe(self._params.on, context)
        run_pipe = self._factory.render_pipe(self._params.run, context)

        self._logger.debug(f"Executing trigger pipe: {self._params.on.id}")
        on_pipe_result: PipeResult = await on_pipe.process(context)

        if on_pipe_result.has_succeeded():
            self._logger.info(f"✅ Trigger succeeded for runner {self._config.id}, executing run pipe")
            run_pipe_result: PipeResult = await run_pipe.process(context)

            if run_pipe_result.succeeded:
                self._logger.info(f"✅ Run pipe {self._params.run.id} completed successfully")
            else:
                self._logger.warning(f"⚠️  Run pipe {self._params.run.id} failed or was skipped")

            return run_pipe_result
        else:
            self._logger.debug(f"⏭️  Trigger failed for runner {self._config.id}: {on_pipe_result.message}")
            return PipeResult.skipped(
                f"The On Pipe did not succeed: {on_pipe_result.message}, so the Run Pipe was not executed."
            )
