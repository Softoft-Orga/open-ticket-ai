from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.pipeline.base_pipe_config import BasePipeConfig

from ..util.pretty_print_config import prettify_dict
from .context import PipelineContext
from .jinja2_env import render_any


class Pipe[ConfigT: BasePipeConfig](ABC):
    def __init__(self, config: ConfigT, *args, **kwargs):
        self.config: ConfigT = config
        self._logger = logging.getLogger(__name__)
        self._pipe_registry: dict[str, type[Pipe]] = {}

    def _build_output(self, state: dict[str, Any], context: PipelineContext) -> PipelineContext:
        new_context: PipelineContext = context.model_copy(deep=True)

        if self.config.name:
            new_context.pipes[self.config.name] = state
        return new_context

    async def _process_steps(self, steps: list[BasePipeConfig], context: PipelineContext) -> PipelineContext:
        """Recursively process all substeps."""
        current_context = context
        for step_config in steps:
            pipe_cls = self._get_pipe_class(step_config.use)
            pipe = pipe_cls(step_config)
            current_context = await pipe.process(current_context)
        return current_context

    def _get_pipe_class(self, pipe_type: str) -> type[Pipe]:
        """Get pipe class from registry or import it."""
        if pipe_type not in self._pipe_registry:
            module_path, class_name = pipe_type.rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            self._pipe_registry[pipe_type] = getattr(module, class_name)
        return self._pipe_registry[pipe_type]

    async def process(self, context: PipelineContext) -> PipelineContext:
        """
        Process the pipeline context through this pipe and its substeps.

        Args:
            context: The current pipeline context

        Returns:
            Updated pipeline context after processing this pipe and all its substeps
        """
        # Initialize pipe data if not present
        if not hasattr(self.config, "data"):
            self.config.data = {}

        self._logger.debug(f"Current context: {prettify_dict(context)}")

        # Render any templated values in the config
        rendered_config = self.config.model_copy(
            update={
                k: render_any(v, context)
                for k, v in self.config.model_dump(exclude_none=True).items()
                if k != "output" and k != "data" and k != "steps"
            }
        )

        self._logger.debug(f"Rendered config: {prettify_dict(rendered_config)}")

        # Check if the pipe should execute
        when_value = rendered_config.when
        if isinstance(when_value, str):
            when_value = when_value.strip().lower() == "true"

        if not when_value:
            self._logger.info(f"Skipping pipe {self.config.name} as 'when' condition is False")
            return context

        # Process substeps first if any
        if hasattr(self.config, "steps") and self.config.steps:
            context = await self._process_steps(self.config.steps, context)

        # Execute the pipe's implementation
        try:
            result = await self._process(context)
            return self._build_output(result, context)
        except Exception as e:
            self._logger.error(f"Error in pipe {self.config.name}: {str(e)}", exc_info=True)
            raise

    @abstractmethod
    async def _process(self, context: PipelineContext) -> dict[str, Any]:
        pass
