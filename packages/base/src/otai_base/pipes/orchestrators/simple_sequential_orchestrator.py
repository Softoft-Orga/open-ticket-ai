import asyncio
from datetime import timedelta
from typing import ClassVar

from pydantic import BaseModel, Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.template_rendering.template_renderer import NoRenderField
from otai_base.pipes.composite_pipe import CompositePipe


class SimpleSequentialOrchestratorParams(StrictBaseModel):
    orchestrator_sleep: timedelta = Field(default=timedelta(seconds=0.01), description="Sleep time in minutes")
    steps: list[PipeConfig] = NoRenderField(default_factory=list, description="Steps to execute")


class SimpleSequentialOrchestrator(CompositePipe[SimpleSequentialOrchestratorParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleSequentialOrchestratorParams

    async def _process_steps(self, context: PipeContext):
        context = context.with_parent(self._params)
        [await self._process_step(step_config, context) for step_config in self._params.steps]

    async def _process(self, context: PipeContext) -> PipeResult:
        while True:
            await self._process_steps(context)
            await asyncio.sleep(self._params.orchestrator_sleep.total_seconds())
