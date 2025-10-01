from __future__ import annotations

import logging
import threading

from injector import inject

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig

from .orchestrator_config import OrchestratorConfig, RunnerDefinition
from .pipe_factory import PipeFactory
from .scheduled_runner import ScheduledPipeRunner


class Orchestrator:
    """Launches scheduled runners for configured pipelines."""

    @inject
    def __init__(self, pipe_factory: PipeFactory, app_config: RawOpenTicketAIConfig) -> None:
        self._pipe_factory = pipe_factory
        self._config = OrchestratorConfig.from_raw(app_config.orchestrator)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._runner_threads: list[threading.Thread] = []
        self._runners: list[ScheduledPipeRunner] = []
        self._running = False

    def _create_runner(self, definition: RunnerDefinition) -> ScheduledPipeRunner:
        return ScheduledPipeRunner(definition, self._pipe_factory)

    def run(self) -> None:
        """Start all configured runners in dedicated daemon threads."""
        if self._running:
            self._logger.debug("Orchestrator already running")
            return

        self._logger.info("Starting orchestrator with %d runner(s)", len(self._config.runners))
        self._runner_threads.clear()
        self._runners.clear()

        for index, definition in enumerate(self._config.runners):
            runner = self._create_runner(definition)
            thread_name = f"ScheduledPipeRunner-{definition.pipe_id}-{index}"
            thread = threading.Thread(target=runner.run, name=thread_name, daemon=True)
            thread.start()
            self._logger.debug("Started runner thread %s", thread_name)
            self._runner_threads.append(thread)
            self._runners.append(runner)

        self._running = True

    def stop(self) -> None:
        """Stop all running runners and wait for their threads to finish."""
        if not self._running:
            self._logger.debug("Orchestrator stop requested but it is not running")
            return

        self._logger.info("Stopping orchestrator")
        for runner in self._runners:
            runner.stop()

        for thread in self._runner_threads:
            thread.join()

        self._runner_threads.clear()
        self._runners.clear()
        self._running = False
