from __future__ import annotations

import logging
from typing import Any
from abc import ABC, abstractmethod

from ..config.registerable import Registerable
from .context import Context
from .pipe_config import PipeResult, RenderedPipeConfig


class Pipe(Registerable, ABC):
    """
    Base class for all pipeline pipes. Public API returns Context, internal logic returns PipeResult.
    """

    def __init__(self, config_raw: dict[str, Any], *args, **kwargs) -> None:
        super().__init__(config_raw, *args, **kwargs)
        self.config = RenderedPipeConfig.model_validate(config_raw)
        self._logger = logging.getLogger(self.__class__.__name__)

    def _save_pipe_result(self, context: Context, pipe_result: PipeResult) -> Context:
        """
        Save the result of this pipe to the context.
        Returns updated Context.
        """
        context.pipes[self.config.id] = pipe_result
        return context

    def have_dependent_pipes_been_run(self, context: Context) -> bool:
        """
        Check if all dependent pipes have succeeded.
        Returns bool.
        """
        return all(context.has_succeeded(dependency_id) for dependency_id in self.config.depends_on)

    async def process(self, context: Context) -> Context:
        """
        Public API. Runs the pipe and returns updated Context.
        """
        self._logger.info("Processing pipe '%s'", self.config.id)
        if self.config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info("Pipe '%s' is running.", self.config.id)
            return await self.__process_and_save(context)
        self._logger.info("Skipping pipe '%s'.", self.config.id)
        return context

    async def __process_and_save(self, context: Context) -> Context:
        """
        Internal. Runs _process and saves result to context.
        Returns updated Context.
        """
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
        """
        Internal business logic. Must be implemented by subclasses.
        Returns PipeResult.
        """
        pass
