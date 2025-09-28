from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic

from open_ticket_ai.core.pipeline.base_pipe_config import ConfigModelType, RawPipeConfig

from ..util.pretty_print_config import prettify_dict
from .context import PipelineContext
from open_ticket_ai.core.config.jinja2_env import render_any


class Pipe(Generic[ConfigModelType], ABC):
    """
    Abstract base class for a pipeline step (a 'pipe').

    It is generic over `ConfigModelType`, which is the specific Pydantic model
    containing the configuration for a given pipe implementation.
    """

    def __init__(self, config: RawPipeConfig[ConfigModelType], *args: Any, **kwargs: Any) -> None:
        self.config: RawPipeConfig[ConfigModelType] = config
        self._logger = logging.getLogger(__name__)
        self._pipe_registry: dict[str, type[Pipe[Any]]] = {}

    def _build_output(self, state: dict[str, Any], context: PipelineContext) -> PipelineContext:
        new_context: PipelineContext = context.model_copy(deep=True)

        if self.config.name:
            new_context.pipes[self.config.name] = state
        return new_context

    async def _process_steps(
        self, steps: list[RawPipeConfig[Any]], context: PipelineContext
    ) -> PipelineContext:
        """Recursively process all substeps."""
        current_context = context
        for step_config in steps:
            pipe_cls = self._get_pipe_class(step_config.use)
            # Here we need to pass the config, but dependencies might be needed.
            # This simplistic instantiation assumes pipes in 'steps' don't have complex deps.
            pipe = pipe_cls(step_config)
            current_context = await pipe.process(current_context)
        return current_context

    def _get_pipe_class(self, pipe_type: str) -> type[Pipe[Any]]:
        """Get pipe class from registry or import it."""
        if pipe_type not in self._pipe_registry:
            module_path, class_name = pipe_type.rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            self._pipe_registry[pipe_type] = getattr(module, class_name)
        return self._pipe_registry[pipe_type]

    async def process(self, context: PipelineContext) -> PipelineContext:
        self._logger.debug(f"Current context: {prettify_dict(context)}")

        # Render any templated values in the config wrapper and the specific config model
        rendered_config = render_any(self.config, context)

        self._logger.debug(f"Rendered config: {prettify_dict(rendered_config)}")

        # Check if the pipe should execute
        when_value = rendered_config.when
        if isinstance(when_value, str):
            when_value = when_value.strip().lower() == "true"

        if not when_value:
            if self.config.name:
                self._logger.info(f"Skipping pipe '{self.config.name}' as 'when' condition is False")
            else:
                self._logger.info(f"Skipping pipe of type '{self.config.use}' as 'when' condition is False")
            return context

        # Process substeps first if any
        if rendered_config.steps:
            context = await self._process_steps(rendered_config.steps, context)

        # Execute the pipe's implementation
        try:
            # The concrete implementation receives the specific, rendered config model
            result = await self._process(context, rendered_config.config)
            return self._build_output(result, context)
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.name}: {str(e)}", exc_info=True)
            raise

    @abstractmethod
    async def _process(self, context: PipelineContext, config: ConfigModelType) -> dict[str, Any]:
        pass
