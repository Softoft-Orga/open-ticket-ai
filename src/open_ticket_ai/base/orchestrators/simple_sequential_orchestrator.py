import asyncio
from datetime import timedelta

from pydantic import Field

from open_ticket_ai.base import CompositePipe
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class SimpleSequentialOrchestratorParams(StrictBaseModel):
    always_rerun: bool = Field(default=True, description="Whether to retry failed steps")
    orchestrator_sleep: timedelta = Field(default=timedelta(seconds=0.01), description="Sleep time in minutes")


class SimpleSequentialOrchestrator(CompositePipe[SimpleSequentialOrchestratorParams]):

    @staticmethod
    def get_params_model() -> type[StrictBaseModel]:
        return SimpleSequentialOrchestratorParams

    async def _process(self, context: PipeContext) -> PipeResult:
        while True:
            await self._process_steps(context)
            await asyncio.sleep(self._params.orchestrator_sleep.total_seconds())
