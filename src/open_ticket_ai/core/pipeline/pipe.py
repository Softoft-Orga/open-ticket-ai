from __future__ import annotations

import logging
from typing import Any

from .context import Context
from .pipe_config import PipeResult, RenderedPipeConfig
from ..config.registerable_class import RegisterableClass


class Pipe(RegisterableClass):

    def __init__(self, config_raw: dict[str, Any], *args, **kwargs) -> None:
        super().__init__(config_raw, *args, **kwargs)
        self.config = RenderedPipeConfig.model_validate(config_raw)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._app_config = kwargs.get("app_config")

    def _save_pipe_result(self, context: Context, pipe_result: PipeResult) -> Context:
        context.pipes[self.config.id] = pipe_result

        return context

    def have_dependent_pipes_been_run(self, context: Context) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self.config.depends_on)

    async def process(self, context: Context) -> Context:
        self._logger.info("Processing pipe '%s'", self.config.id)

        if self.config._if and self.have_dependent_pipes_been_run(context):
            return await self.__process_and_save(context)

        return context

    async def __process_and_save(self, context: Context) -> Context:

        new_context = context.model_copy()

        try:

            pipe_result = await self._process()

        except Exception as e:

            self._logger.error(f"Error in pipe {self.config.id}: {str(e)}", exc_info=True)

            pipe_result = PipeResult(success=False, failed=True, message=str(e))

        updated_context = self._save_pipe_result(new_context, pipe_result)

        return updated_context

    async def _process(self) -> PipeResult:

        pass
