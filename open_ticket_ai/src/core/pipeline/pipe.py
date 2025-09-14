# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel

from .context import PipelineContext
from ..config.config_models import OpenTicketAIConfig


class Pipe[InputDataT: BaseModel, OutputDataT: BaseModel](ABC):
    InputModel: ClassVar[type[BaseModel]]
    OutputModel: ClassVar[type[BaseModel]]

    def __init__(self, config: OpenTicketAIConfig):
        self.config: OpenTicketAIConfig = config

    @abstractmethod
    async def process(self, context: PipelineContext[InputDataT]) -> PipelineContext[OutputDataT]:
        pass
