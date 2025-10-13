from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict

from ..config.renderable import Renderable
from ..logging_iface import LoggerFactory
from .pipe_config import PipeConfig, PipeResult
from .pipe_context import PipeContext

class ParamsModel(BaseModel):
    model_config = ConfigDict(extra="allow")

class Pipe[ParamsT: ParamsModel](Renderable, ABC):
    params_class: type[ParamsT]

    def __init__(
        self, pipe_params: PipeConfig[ParamsT], logger_factory: LoggerFactory, *args: Any, **kwargs: Any
    ) -> None:
        self.pipe_config = pipe_params
        self._logger = logger_factory.get_logger(self.__class__.__name__)

        if isinstance(pipe_params.params, dict):
            self.params: ParamsT = self.params_class.model_validate(pipe_params.params)
        else:
            self.params: ParamsT = pipe_params.params

    def _save_pipe_result(self, context: PipeContext, pipe_result: PipeResult[Any]) -> PipeContext:
        if self.pipe_config.id is not None:
            context.pipes[self.pipe_config.id] = pipe_result
        return context

    def have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self.pipe_config.depends_on)

    async def process(self, context: PipeContext) -> PipeContext:
        self._logger.info(f"Processing pipe '{self.pipe_config.id}'")
        if self.pipe_config.should_run and self.have_dependent_pipes_been_run(context):
            self._logger.info(f"Pipe '{self.pipe_config.id}' is running.")
            return await self.__process_and_save(context)
        self._logger.info(f"Skipping pipe '{self.pipe_config.id}'.")
        return context

    async def __process_and_save(self, context: PipeContext) -> PipeContext:
        new_context = context.model_copy()
        try:
            pipe_result = await self._process()
        except Exception as e:
            self._logger.error(f"Error in pipe {self.pipe_config.id}: {str(e)}", exc_info=True)
            pipe_result = PipeResult[ParamsModel](success=False, failed=True, message=str(e), data=ParamsModel())
        updated_context = self._save_pipe_result(new_context, pipe_result)
        return updated_context

    @abstractmethod
    async def _process(self) -> PipeResult[Any]:
        pass
