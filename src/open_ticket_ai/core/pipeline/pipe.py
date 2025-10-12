from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from ..config.renderable import Renderable
from .pipe_config import PipeConfig, PipeResult
from .pipe_context import PipeContext


class Pipe[ParamsT](Renderable, ABC):
    def __init__(self, pipe_params: PipeConfig[ParamsT], *args: Any, **kwargs: Any) -> None:
        super().__init__(pipe_params.params, *args, **kwargs)
        self.pipe_config = pipe_params
        self._logger = logging.getLogger(self.__class__.__name__)

    def _save_pipe_result(self, context: PipeContext, pipe_result: PipeResult) -> PipeContext:
        context.pipes[self.pipe_config.id] = pipe_result
        return context

    def have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self.pipe_config.depends_on)

    async def process(self, context: PipeContext) -> PipeContext:
        self._logger.info("Processing pipe '%s'", self.pipe_config.id)
        if self.pipe_config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info("Pipe '%s' is running.", self.pipe_config.id)
            return await self.__process_and_save(context)
        self._logger.info("Skipping pipe '%s'.", self.pipe_config.id)
        return context

    async def __process_and_save(self, context: PipeContext) -> PipeContext:
        new_context = context.model_copy()
        try:
            pipe_result = await self._process()
        except Exception as e:
            self._logger.error(f"Error in pipe {self.pipe_config.id}: {str(e)}", exc_info=True)
            pipe_result = PipeResult(success=False, failed=True, message=str(e), data=BaseModel())
        updated_context = self._save_pipe_result(new_context, pipe_result)
        return updated_context

    @abstractmethod
    async def _process(self) -> PipeResult:
        pass
