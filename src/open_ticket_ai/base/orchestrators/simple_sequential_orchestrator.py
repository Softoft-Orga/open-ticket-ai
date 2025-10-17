import asyncio
from datetime import timedelta

from pydantic import Field, BaseModel

from open_ticket_ai.base import CompositePipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class SimpleSequentialOrchestratorParams(BaseModel):
    always_rerun: bool = Field(default=True, description="Whether to retry failed steps")
    orchestrator_sleep: timedelta = Field(default=timedelta(seconds=0.01), description="Sleep time in minutes")


class SimpleSequentialOrchestrator(CompositePipe[SimpleSequentialOrchestratorParams]):

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return SimpleSequentialOrchestratorParams

    async def _process_steps(self, context: PipeContext):
        context = context.model_copy(update={"parent": context.params})
        [await self._process_step(step_config, context) for step_config in self._config.steps or []]

    async def _process(self, context: PipeContext) -> PipeResult:
        while True:
            await self._process_steps(context)
            await asyncio.sleep(self._params.orchestrator_sleep.total_seconds())
