from __future__ import annotations

from injector import inject, singleton

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_models import (
    OrchestratorConfig,
    RunnerDefinition,
)
from open_ticket_ai.core.orchestration.pipe_runner import PipeRunner
from open_ticket_ai.core.orchestration.trigger import Trigger
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


@singleton
class Orchestrator:
    @inject
    def __init__(
            self,
            renderable_factory: RenderableFactory,
            orchestrator_config: OrchestratorConfig,
            logger_factory: LoggerFactory,
    ) -> None:
        self._renderable_factory = renderable_factory
        self._config = orchestrator_config
        self._logger = logger_factory.create(self.__class__.__name__)
        self._logger_factory = logger_factory
        self._runners: dict[str, PipeRunner] = {}
        self._triggers: list[Trigger] = []

    def _create_pipe_runners(self):
        self._runners = {
            runner_def.get_id(): self._create_pipe_runner(runner_def) for runner_def in self._config.runners
        }

    def _create_pipe_runner(self, runner_id_def: RunnerDefinition) -> PipeRunner | None:
        pipe = self._renderable_factory.render(runner_id_def.run, PipeContext())
        return PipeRunner(runner_id_def.id, pipe, self._logger_factory)

    def _create_triggers(self):
        for runner_def in self._config.runners:
            for trigger_def in runner_def.on:
                trigger: Trigger = self._renderable_factory.render(trigger_def, PipeContext())
                trigger.attach(self._runners[runner_def.get_id()])

    def init(self):
        self._create_pipe_runners()
        self._create_triggers()

    async def run(self):
        for trigger in self._triggers:
            await trigger.run()
