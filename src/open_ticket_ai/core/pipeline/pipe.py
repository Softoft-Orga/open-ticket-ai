from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Generic, TypeVar, Type

from ..config.base_pipe_config import BasePipeConfig

ConfigT = TypeVar("ConfigT", bound=BasePipeConfig)

from .context import PipelineContext
from .jinja2_env import render_any
from ..config.base_pipe_config import BasePipeConfig


class Pipe(ABC, Generic[ConfigT]):
    ConfigModel: Type[ConfigT] = BasePipeConfig  # type: ignore

    def __init__(self, config: ConfigT, *args, **kwargs):
        self.config: ConfigT = config
        self._logger = logging.getLogger(__name__)

    def _build_output(self, state: Dict[str, Any], context: PipelineContext) -> PipelineContext:
        if not state:
            return context

        new_context: PipelineContext = context.model_copy(deep=True)
        new_context.current_state = state
        self._logger.info(f"New context: {new_context}\n\n")
        rendered_output = {k: render_any(v, new_context) for k, v in self.config.output.items()}
        self._logger.info(f"Rendered output: {rendered_output}\n\n")
        def deep_merge(d1, d2):
            for k, v in d2.items():
                if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
                    deep_merge(d1[k], v)
                else:
                    d1[k] = v
            return d1
            
        data_merged = deep_merge(new_context.model_dump(), rendered_output)
        new_context = PipelineContext.model_validate(data_merged)
        self._logger.info(f"Output merged: {new_context}\n\n")
        return new_context
    async def process(self, context: PipelineContext) -> PipelineContext:
        context.current_state = {}
        self._logger.info(f"Current context: {context}\n\n")
        updated = self.config.model_copy(
            update={k: render_any(v, context) for k, v in self.config.model_dump(exclude_none=True).items() if
                    k != "output"}
        )
        self._logger.debug(f"Updated config: {updated}")
        when_value = updated.when
        if isinstance(updated.when, str):
            when_value = when_value.strip().lower() == "true"

        if not isinstance(when_value, bool):
            raise ValueError(f"'when' condition must evaluate to a boolean, got {when_value}")

        if not when_value:
            self._logger.info(f"Skipping {self.__class__.__name__} due to 'when' condition being False.")
            return context

        new_state = await self._process(updated)
        return self._build_output(new_state, context)

    @abstractmethod
    async def _process(self, rendered_config: ConfigT) -> Dict[str, Any]:
        pass
