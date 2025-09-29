from __future__ import annotations

import logging
import typing
from abc import abstractmethod
from typing import Any, Self

from ..config import jinja2_env
from ..config.registerable_config import RegisterableConfig
from .context import Context


class ConfigurablePipe:
    def __init__(
            self, config: dict[str, Any]
    ) -> None:
        self.config = RegisterableConfig(**config)
        self._logger = logging.getLogger(__name__)

    def _save_state(self, context: Context, state: dict[str, Any]) -> Context:
        context.pipes[self.config.name] = state
        return context

    def _build_pipe_from_step_config(self, step_config: dict[str, Any], context: Context) -> Self:
        rendered_step_config = jinja2_env.render_recursive(step_config, context)
        pipe_class = typing.cast(type[Self], rendered_step_config["use"])
        return pipe_class(rendered_step_config)

    async def _process_steps(self, context: Context):
        for step_pipe_config in self.config.steps:
            step_pipe = self._build_pipe_from_step_config(step_pipe_config, context)
            self._current_context = await step_pipe.process(context)

    async def process(self, context: Context) -> Context:
        if not self.config.when:
            self._logger.info(
                f"Skipping pipe '{self.config.name}' of type '{self.__class__.__name__}' as 'when' condition is False"
            )
            return context

        await self._process_steps(context)

        try:
            result = await self._process()
            return self._save_state(context, result)
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.name}: {str(e)}", exc_info=True)
            raise e

    @abstractmethod
    async def _process(self) -> dict[str, Any]:
        pass
