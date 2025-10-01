from __future__ import annotations

import asyncio
import logging
import threading
from copy import deepcopy

from injector import inject

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory

from .orchestrator_config import RunnerDefinition


class ScheduledPipeRunner:
    """Continuously executes a configured pipe on a fixed interval."""

    @inject
    def __init__(self, definition: RunnerDefinition, pipe_factory: PipeFactory):
        self._definition = definition
        self._pipe_factory = pipe_factory
        self._stop_event = threading.Event()
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def definition(self) -> RunnerDefinition:
        return self._definition

    def stop(self) -> None:
        """Signal the runner to stop after the current iteration."""
        self._stop_event.set()

    def _build_context(self) -> Context:
        return Context(config=deepcopy(self._definition.pipe))

    def _create_pipe(self, context: Context):
        return self._pipe_factory.create_pipe({}, deepcopy(self._definition.pipe), context.model_dump())

    def run(self) -> None:
        """Run the configured pipe until :py:meth:`stop` is called."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while not self._stop_event.is_set():
                context = self._build_context()
                try:
                    pipe = self._create_pipe(context)
                    loop.run_until_complete(pipe.process(context))
                except Exception:  # pragma: no cover - defensive programming
                    self._logger.exception("Pipe execution failed")
                interval = self._definition.interval_seconds
                if interval <= 0:
                    continue
                if self._stop_event.wait(interval):
                    break
        finally:
            asyncio.set_event_loop(None)
            loop.close()
