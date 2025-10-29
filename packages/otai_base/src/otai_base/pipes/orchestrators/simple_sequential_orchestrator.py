import asyncio
from datetime import timedelta
from typing import Annotated, ClassVar

from open_ticket_ai import NoRenderField, StrictBaseModel
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from pydantic import BaseModel, Field

from otai_base.pipes.composite_pipe import CompositePipe


class SimpleSequentialOrchestratorParams(StrictBaseModel):
    orchestrator_sleep: timedelta = Field(default=timedelta(seconds=0.01), description="Sleep time in minutes")
    exception_sleep: timedelta = Field(default=timedelta(seconds=5), description="Sleep time in minutes")
    always_retry: bool = Field(default=True, description="Whether to always retry failed steps")
    steps: Annotated[list[PipeConfig], NoRenderField(default_factory=list, description="Steps to execute")]


class SimpleSequentialOrchestrator(CompositePipe[SimpleSequentialOrchestratorParams]):
    ParamsModel: ClassVar[type[BaseModel]] = SimpleSequentialOrchestratorParams

    async def _process_steps(self, context: PipeContext):
        context = context.with_parent(self._params)
        for step_config in self._params.steps:
            await self._process_step(step_config, context)

    async def _process(self, context: PipeContext) -> PipeResult:
        while True:
            try:
                self._logger.debug("Orchestrator cycle started")
                await self._process_steps(context)
                await asyncio.sleep(self._params.orchestrator_sleep.total_seconds())

            except Exception:
                self._logger.exception("Orchestrator encountered an error")
                if not self._params.always_retry:
                    raise
                await asyncio.sleep(self._params.exception_sleep.total_seconds())
