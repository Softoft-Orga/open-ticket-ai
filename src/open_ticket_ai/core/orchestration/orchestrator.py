from __future__ import annotations

import asyncio

from injector import inject, singleton

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_models import (
    OrchestratorConfig,
    TriggerConfig,
)
from open_ticket_ai.core.orchestration.scheduled_runner import PipeRunner
from open_ticket_ai.core.orchestration.trigger import Trigger
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


@singleton
class Orchestrator:
    @inject
    def __init__(
        self, pipe_factory: RenderableFactory, orchestrator_config: OrchestratorConfig, logger_factory: LoggerFactory
    ) -> None:
        self._pipe_factory = pipe_factory
        self._config = orchestrator_config
        self._logger = logger_factory.create(self.__class__.__name__)
        self._logger_factory = logger_factory
        self._trigger_registry: dict[str, Trigger] = {}
        self._runners: dict[str, PipeRunner] = {}

    def _instantiate_trigger(self, trigger_def: TriggerConfig) -> Trigger:
        scope = PipeContext()
        return self._pipe_factory.render(trigger_def, scope)

    def start(self) -> None:
        for index, definition in enumerate(self._config.runners):
            runner = PipeRunner(definition, self._pipe_factory, self._logger_factory)
            job_id = f"{definition.pipe_id}_{index}"
            self._runners[job_id] = runner
            for trigger_def in definition.on:
                trigger = self._trigger_registry.get(trigger_def.id) or self._instantiate_trigger(trigger_def)
                self._trigger_registry[trigger_def.id] = trigger
                trigger.attach(runner)
        for trigger in self._trigger_registry.values():
            trigger.start()

    def stop(self) -> None:
        self._logger.info("Stopping orchestrator")
        for trigger in self._trigger_registry.values():
            trigger.stop()
        self._trigger_registry.clear()
        self._runners.clear()
        self._logger.info("Orchestrator stopped successfully")

    async def run(self) -> None:
        self.start()
        try:
            await asyncio.Future()  # Run forever
        except Exception as e:
            self._logger.info(f"{e.__class__.__name__} received; shutting down orchestrator")
            self.stop()
