from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from ..config.registerable import Registerable
from .pipe_context import PipeContext
from .pipe_config import PipeResult, RenderedPipeConfig


class Pipe(Registerable, ABC):
    def __init__(self, config: RenderedPipeConfig, *args, **kwargs) -> None:
        super().__init__(config, *args, **kwargs)
        self.config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    def _save_pipe_result(self, context: PipeContext, pipe_result: PipeResult) -> PipeContext:
        context.pipes[self.config.id] = pipe_result
        return context

    def have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self.config.depends_on)

    async def process(self, context: PipeContext) -> PipeContext:
        self._logger.info("Processing pipe '%s'", self.config.id)
        if self.config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info("Pipe '%s' is running.", self.config.id)
            return await self.__process_and_save(context)
        self._logger.info("Skipping pipe '%s'.", self.config.id)
        return context

    async def __process_and_save(self, context: PipeContext) -> PipeContext:
        new_context = context.model_copy()
        try:
            pipe_result = await self._process()
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.id}: {str(e)}", exc_info=True)
            pipe_result = PipeResult(success=False, failed=True, message=str(e))
        updated_context = self._save_pipe_result(new_context, pipe_result)
        return updated_context

    @abstractmethod
    async def _process(self) -> PipeResult:
        pass
