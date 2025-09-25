# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from jinja2.environment import TemplateExpression
from pydantic import BaseModel

from .context import PipelineContext
from .jinja2_env import render_any, _env
from ..config.base_pipe_config import BasePipeConfig


class Pipe(ABC):
    def __init__(self, config: BasePipeConfig):
        self.config = config
        self.when_expression: TemplateExpression = _env.compile_expression(config.when)
        self._logger = logging.getLogger(__name__)

    async def process(self, context: PipelineContext) -> PipelineContext:
        confid_dict = self.config.model_dump()
        rendered_dict = {k: render_any(v, context) for k, v in confid_dict.items()}
        should_process = bool(self.when_expression(**context.model_dump()))
        if not should_process:
            self._logger.info(f"Skipping {self.__class__.__name__} due to 'when' condition evaluating to False.")
            return context
        return await self._process(context, self.config.model_validate(rendered_dict))

    @abstractmethod
    async def _process(self, context: PipelineContext, rendered_config: BaseModel) -> PipelineContext:
        pass
