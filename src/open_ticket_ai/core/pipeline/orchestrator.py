from __future__ import annotations

import asyncio
import logging
from importlib import import_module
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from injector import inject, singleton

from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig, RunnerDefinition, TriggerDefinition
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.pipeline.scheduled_runner import ScheduledPipeRunner


@singleton
class Orchestrator:
    """Manages scheduled pipeline execution using APScheduler."""

    @inject
    def __init__(self, pipe_factory: PipeFactory, orchestrator_config: OrchestratorConfig) -> None:
        self._pipe_factory = pipe_factory
        self._config = orchestrator_config
        self._logger = logging.getLogger(self.__class__.__name__)
        self._scheduler = AsyncIOScheduler()
        self._runners: dict[str, ScheduledPipeRunner] = {}

    def _create_runner(self, definition: RunnerDefinition) -> ScheduledPipeRunner:
        return ScheduledPipeRunner(definition, self._pipe_factory)

    def _instantiate_trigger(self, trigger_def: TriggerDefinition) -> Any:
        module_path, class_name = trigger_def.use.rsplit(":", 1)
        module = import_module(module_path)
        trigger_class = getattr(module, class_name)
        return trigger_class(**trigger_def.params)

    def start(self) -> None:
        """Start the orchestrator and all scheduled runners."""
        if self._scheduler.running:
            self._logger.debug("Orchestrator already running")
            return

        self._logger.info("Starting orchestrator with %d runner(s)", len(self._config.runners))

        for index, definition in enumerate(self._config.runners):
            runner = self._create_runner(definition)
            job_id = f"{definition.pipe_id}_{index}"
            self._runners[job_id] = runner

            max_instances = 1
            if definition.settings and definition.settings.concurrency:
                max_instances = definition.settings.concurrency.max_workers

            if definition.triggers:
                for trigger_index, trigger_def in enumerate(definition.triggers):
                    trigger = self._instantiate_trigger(trigger_def)
                    trigger_job_id = f"{job_id}_trigger_{trigger_index}"
                    
                    self._scheduler.add_job(
                        runner.execute,
                        trigger=trigger,
                        id=trigger_job_id,
                        name=f"Pipe: {definition.pipe_id} (trigger: {trigger_def.id})",
                        max_instances=max_instances,
                        coalesce=True,
                    )
                    self._logger.info(
                        "Scheduled pipe '%s' with trigger '%s' (%s)",
                        definition.pipe_id,
                        trigger_def.id,
                        trigger_def.use,
                    )
            else:
                self._scheduler.add_job(
                    runner.execute,
                    id=job_id,
                    name=f"Pipe: {definition.pipe_id} (one-time)",
                )
                self._logger.info("Scheduled pipe '%s' for one-time execution", definition.pipe_id)

        self._scheduler.start()
        self._logger.info("Orchestrator started successfully")

    def stop(self) -> None:
        """Stop the orchestrator and all scheduled runners gracefully."""
        if not self._scheduler.running:
            self._logger.debug("Orchestrator stop requested but it is not running")
            return

        self._logger.info("Stopping orchestrator")
        self._scheduler.shutdown()
        self._runners.clear()
        self._logger.info("Orchestrator stopped successfully")

    async def run(self) -> None:
        """Start the orchestrator and keep it running. Blocks until shutdown."""
        self.start()

        try:
            while self._scheduler.running:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            self._logger.info("%s received; shutting down orchestrator", e.__class__.__name__)
            self._logger.info("Shutdown signal received; Ending orchestrator")
            self.stop()

        finally:
            self.stop()
