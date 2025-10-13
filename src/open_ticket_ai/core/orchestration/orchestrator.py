from __future__ import annotations

import asyncio
from typing import Any

from injector import inject, singleton

from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_config import (
    OrchestratorConfig,
    TriggerDefinition,
)
from open_ticket_ai.core.orchestration.scheduled_runner import PipeRunner
from open_ticket_ai.core.orchestration.trigger import Trigger
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


@singleton
class Orchestrator:
    """Manages pipeline execution using Observer Pattern for triggers."""

    @inject
    def __init__(
        self, pipe_factory: RenderableFactory, orchestrator_config: OrchestratorConfig, logger_factory: LoggerFactory
    ) -> None:
        self._pipe_factory = pipe_factory
        self._config = orchestrator_config
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        self._trigger_registry: dict[str, Trigger[Any]] = {}
        self._runners: dict[str, PipeRunner] = {}

    def _instantiate_trigger(self, trigger_def: TriggerDefinition[Any]) -> Trigger[Any]:
        """Instantiate trigger using RenderableFactory for consistency with pipe instantiation."""
        scope = PipeContext()
        trigger: Trigger[Any] = self._pipe_factory.create_trigger(trigger_def, scope)  # type: ignore[assignment]
        return trigger

    def start(self) -> None:
        """Start the orchestrator and all runners."""
        self._logger.info(f"Starting orchestrator with {len(self._config.runners)} runner(s)")

        for index, definition in enumerate(self._config.runners):
            runner = PipeRunner(definition, self._pipe_factory)
            job_id = f"{definition.pipe_id}_{index}"
            self._runners[job_id] = runner

            for _trigger_index, trigger_def in enumerate(definition.on):
                # Ensure trigger has a valid ID (never None)
                trigger_id = trigger_def.id
                if trigger_id is None:
                    raise ValueError(
                        f"Trigger in runner '{definition.pipe_id}' has no ID. "
                        f"All triggers must have a unique 'id' field."
                    )

                if trigger_id in self._trigger_registry:
                    trigger = self._trigger_registry[trigger_id]
                else:
                    trigger = self._instantiate_trigger(trigger_def)
                    self._trigger_registry[trigger_id] = trigger

                trigger.attach(runner)
                self._logger.info(
                    f"Attached pipe '{definition.pipe_id}' to trigger '{trigger_def.id}' ({trigger_def.use})"
                )

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
            self._logger.info(f"{e.__class__.__name__} received; shutting down orchestrator")
            self.stop()
