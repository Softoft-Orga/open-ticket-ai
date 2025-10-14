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
    
    def __getitem__(self, key: str) -> Any:
        """Allow dict-style access to params for backward compatibility."""
        return getattr(self, key)


class Pipe(Renderable, ABC):
    # Optional: Child classes can set this to enable automatic params validation
    params_class: type[ParamsModel] | None = None
    
    def __init__(self, pipe_config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.pipe_config = pipe_config
        self._logger = logger_factory.get_logger(self.__class__.__name__)
        
        # Validate params if params_class is specified
        if self.params_class is not None and isinstance(pipe_config.params, dict):
            # Convert dict to validated Pydantic model
            self.params: Any = self.params_class.model_validate(pipe_config.params)
        else:
            # Keep params as-is (could be dict or already a Pydantic model)
            self.params: dict[str, Any] = pipe_config.params

    def _save_pipe_result(self, context: PipeContext, pipe_result: PipeResult) -> PipeContext:
        if self.pipe_config.id is not None:
            context.pipes[self.pipe_config.id] = pipe_result
        return context

    def have_dependent_pipes_been_run(self, context: PipeContext) -> bool:
        return all(context.has_succeeded(dependency_id) for dependency_id in self.pipe_config.depends_on)

    async def process(self, context: PipeContext) -> PipeContext:
        """Process the pipe with the given context.
        
        This method checks if the pipe should be skipped (based on if_ condition),
        validates dependencies, and executes the pipe's _process method.
        """
        # Check if pipe should be skipped based on if_ condition
        if self.pipe_config.if_ is False:
            return context
        
        # Check if dependencies have been satisfied
        if not self.have_dependent_pipes_been_run(context):
            self._logger.warning(f"Pipe {self.pipe_config.id} skipped: dependencies not satisfied")
            return context
        
        return await self.__process_and_save(context)

    async def __process_and_save(self, context: PipeContext) -> PipeContext:
        new_context = context.model_copy()
        try:
            pipe_result = await self._process()
        except Exception as e:
            self._logger.error(f"Error in pipe {self.pipe_config.id}: {str(e)}", exc_info=True)
            pipe_result = PipeResult(success=False, failed=True, message=str(e), data=ParamsModel())
        updated_context = self._save_pipe_result(new_context, pipe_result)
        return updated_context

    @abstractmethod
    async def _process(self) -> PipeResult:
        pass
