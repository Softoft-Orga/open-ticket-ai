from __future__ import annotations

import logging
from copy import deepcopy

from injector import inject

from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory

from .orchestrator_config import RunnerDefinition


class ScheduledPipeRunner:
    """Executes a pipeline on demand. Designed to be called by APScheduler."""

    @inject
    def __init__(self, definition: RunnerDefinition, pipe_factory: PipeFactory):
        self._definition = definition
        self._pipe_factory = pipe_factory
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def definition(self) -> RunnerDefinition:
        return self._definition

    def _build_context(self) -> Context:
        return Context(config=deepcopy(self._definition.pipe))

    def _create_pipe(self, context: Context):
        return self._pipe_factory.create_pipe({}, deepcopy(self._definition.pipe), context.model_dump())

    async def execute(self) -> None:
        """Execute the pipe once. Called by APScheduler."""
        self._logger.debug("Executing pipe '%s'", self._definition.pipe_id)
        
        context = self._build_context()
        try:
            pipe = self._create_pipe(context)
            await pipe.process(context)
            self._logger.info("Pipe '%s' executed successfully", self._definition.pipe_id)
        except Exception:
            self._logger.exception("Pipe '%s' execution failed", self._definition.pipe_id)
            raise  # Re-raise so APScheduler can track failures
