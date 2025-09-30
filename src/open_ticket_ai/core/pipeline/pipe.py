from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any

from .context import Context
from .pipe_config import PipeResult, RenderedPipeConfig
from .pipe_factory import PipeFactory
from ..config.registerable_class import RegisterableClass
from ..config.registerable_config import RegisterableConfig


class Pipe(RegisterableClass):
    def __init__(self, config_raw: dict[str, Any], factory: PipeFactory | None = None, *args, **kwargs) -> None:
        config = RegisterableConfig.model_validate(config_raw)
        super().__init__(config, *args, **kwargs)
        self.config = RenderedPipeConfig.model_validate(config_raw)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._factory = factory

    def _save_state(self, context: Context, state: PipeResult) -> Context:
        context.pipes[self.config.name] = state
        return context

    def have_dependent_pipes_been_run(self, context: Context) -> bool:
        for dependency_id in self.config.depends_on:
            if not context.has_succeeded(dependency_id):
                return False
        return True

    async def process(self, context: Context) -> Context:
        # noinspection PyProtectedMember
        if self.config._if and self.have_dependent_pipes_been_run(context):
            return await self.__process_and_safe(context)
        return context

    async def __process_and_safe(self, context: Context) -> Context:
        new_context = context
        try:
            result_data = await self._process()
            pipe_result = PipeResult(success=True, failed=False, data=result_data)
            new_context = self._save_state(context, pipe_result)
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.name}: {str(e)}", exc_info=True)
            failure_result = PipeResult(success=False, failed=True, message=str(e), data={})
            new_context = self._save_state(context, failure_result)
        return new_context

    async def _process(self) -> dict[str, Any]:
        pass
