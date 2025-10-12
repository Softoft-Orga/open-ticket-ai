from __future__ import annotations

import asyncio
import logging
from importlib import import_module

from injector import inject, singleton

from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.orchestration.orchestrator_config import (
    OrchestratorConfig,
    TriggerDefinition,
)
from open_ticket_ai.core.orchestration.scheduled_runner import PipeRunner
from open_ticket_ai.core.orchestration.trigger import Trigger


@singleton
class Orchestrator:
    """Manages pipeline execution using Observer Pattern for triggers."""

    @inject
    def __init__(self, pipe_factory: RenderableFactory, orchestrator_config: OrchestratorConfig) -> None:
        self._pipe_factory = pipe_factory
        self._config = orchestrator_config
        self._logger = logging.getLogger(self.__class__.__name__)
        self._trigger_registry: dict[str, Trigger] = {}
        self._runners: dict[str, PipeRunner] = {}

    def _instantiate_trigger(self, trigger_def: TriggerDefinition) -> Trigger:
        module_path, class_name = trigger_def.use.rsplit(":", 1)
        module = import_module(module_path)
        trigger_class = getattr(module, class_name)
        return trigger_class(trigger_def)

    def start(self) -> None:
        """Start the orchestrator and all runners."""
        self._logger.info("Starting orchestrator with %d runner(s)", len(self._config.runners))

        for index, definition in enumerate(self._config.runners):
            runner = PipeRunner(definition, self._pipe_factory)
            job_id = f"{definition.pipe_id}_{index}"
            self._runners[job_id] = runner

            if definition.on:
                for _trigger_index, trigger_def in enumerate(definition.on):
                    trigger_id = trigger_def.id
                    if trigger_id in self._trigger_registry:
                        trigger = self._trigger_registry[trigger_id]
                    else:
                        trigger = self._instantiate_trigger(trigger_def)
                        self._trigger_registry[trigger_id] = trigger

                    trigger.attach(runner)
                    self._logger.info(
                        "Attached pipe '%s' to trigger '%s' (%s)",
                        definition.pipe_id,
                        trigger_def.id,
                        trigger_def.use,
                    )
            else:
                # One-time execution
                asyncio.create_task(runner.execute())
                self._logger.info("Scheduled pipe '%s' for one-time execution", definition.pipe_id)

        # Start all triggers
        for trigger in self._trigger_registry.values():
            trigger.start()

        self._logger.info("Orchestrator started successfully")

    def stop(self) -> None:
        """Stop the orchestrator and all triggers."""
        self._logger.info("Stopping orchestrator")
        for trigger in self._trigger_registry.values():
            trigger.stop()
        self._trigger_registry.clear()
        self._runners.clear()
        self._logger.info("Orchestrator stopped successfully")

    async def run(self) -> None:
        """Start the orchestrator and keep it running. Blocks until shutdown."""
        self.start()

        try:
            await asyncio.Future()  # Run forever
        except (KeyboardInterrupt, SystemExit) as e:
            self._logger.info("%s received; shutting down orchestrator", e.__class__.__name__)
            self.stop()
