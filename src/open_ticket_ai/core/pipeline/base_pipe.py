from __future__ import annotations

import logging
import typing
from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from .base_pipe_config import RawPipeConfig, RenderedPipeConfig, PipeConfig
from .context import PipelineContext
from ..config.raw_config import RenderableConfig
from ..config.registerable_class import RegisterableClass


class BasePipe[RawPipeConfigT: RawPipeConfig, RenderedPipeConfigT: RenderedPipeConfig](
    RegisterableClass[RawPipeConfigT, RenderedPipeConfigT]
):

    def __init__(self, config: PipeConfig, *args: Any,
                 **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self._current_context: PipelineContext = PipelineContext()

    @property
    def config(self):
        self._config.save_rendered(self._current_context)
        return super().config

    def _build_output(self, state: dict[str, Any]) -> PipelineContext:
        self._current_context.pipes[self.config.name] = state
        return self._current_context

    async def _process_steps(self):
        for step_pipe in self.config.steps:
            self._current_context = await step_pipe.process(self._current_context)

    async def process(self, context: PipelineContext) -> PipelineContext:
        self._current_context = context
        if not self.config.when:
            self._logger.info(
                f"Skipping pipe '{self.config.name}' of type '{self.__class__.__name__}' as 'when' condition is False")
            return context

        await self._process_steps()

        try:
            result = await self._process()
            return self._build_output(result)
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.name}: {str(e)}", exc_info=True)
            raise e

    @abstractmethod
    async def _process(self) -> dict[str, Any]:
        pass
