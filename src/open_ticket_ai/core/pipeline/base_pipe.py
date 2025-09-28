from __future__ import annotations

import logging
import typing
from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig
from .context import PipelineContext
from ..config.template_configured_class import TemplateConfiguredClass


class BasePipe[RawConfigT: RawPipeConfig](ABC, TemplateConfiguredClass):
    @staticmethod
    @abstractmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        pass

    def __init__(
            self,
            config: RawPipeConfig[RawConfigT],
            registry: UnifiedRegistry | None = None,
            *args: Any,
            **kwargs: Any
    ) -> None:
        self.__raw_pipe_config: RawPipeConfig[RawConfigT] = config
        self._registry = registry
        self._logger = logging.getLogger(__name__)
        self._current_context: PipelineContext = PipelineContext()

    @property
    def config(self) :
        return self.__raw_pipe_config.render(self._current_context)

    def _build_output(self, state: dict[str, Any]) -> PipelineContext:
        self._current_context.pipes[self.config.name] = state
        return self._current_context

    async def _process_steps(self):
        for step_config in self.__raw_pipe_config.steps:
            pipe_class = self._get_pipe_class(step_config.render(self._current_context).use)
            pipe_instance = pipe_class(config=step_config, registry=self._registry)
            self._current_context = await pipe_instance.process(self._current_context)

    def _get_pipe_class(self, pipe_type: str) -> type[BasePipe[Any]]:
        return typing.cast(type[BasePipe[Any]], self._registry.get_class(pipe_type))

    async def process(self, context: PipelineContext) -> PipelineContext:
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
            raise

    @abstractmethod
    async def _process(self) -> dict[str, Any]:
        pass
