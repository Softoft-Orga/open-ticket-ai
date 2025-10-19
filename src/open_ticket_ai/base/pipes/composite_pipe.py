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

    def __init__(self, factory: PipeFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._factory: PipeFactory = factory

    async def _process_steps(self, context: PipeContext) -> list[PipeResult]:
        step_count = len(self._config.steps or [])
        self._logger.info(f"🔄 Processing {step_count} step(s) in composite pipe: {self._config.id}")

        context = context.model_copy(update={"parent": context.params})
        results = []

        for idx, step_config in enumerate(self._config.steps or [], 1):
            self._logger.debug(f"Step {idx}/{step_count}: {step_config.id}")

            result = await self._process_step(step_config, context)
            context = context.with_pipe_result(step_config.id, result)
            results.append(result)

            if result.succeeded:
                self._logger.debug(f"Step {step_config.id} succeeded")
            elif result.skipped:
                self._logger.debug(f"Step {step_config.id} was skipped")
            else:
                self._logger.warning(f"Step {step_config.id} failed: {result.message}")

        succeeded = sum(1 for r in results if r.succeeded)
        failed = sum(1 for r in results if not r.succeeded and not r.skipped)
        skipped = sum(1 for r in results if r.skipped)

        self._logger.info(
            f"📊 Composite pipe {self._config.id} completed: {succeeded} succeeded, {failed} failed, {skipped} skipped"
        )

        return results

    @final
    async def _process_step(self, step_config: PipeConfig, context: PipeContext) -> PipeResult:
        step_pipe = self._factory.render_pipe(step_config, context)
        return await step_pipe.process(context)

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.union(await self._process_steps(context))
