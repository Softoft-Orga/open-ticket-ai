# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel

from .context import PipelineContext


class Pipe[InputDataT: BaseModel, OutputDataT: BaseModel](ABC):
    InputModel: ClassVar[type[BaseModel]]
    OutputModel: ClassVar[type[BaseModel]]

    @abstractmethod
    async def process(self, context: PipelineContext[InputDataT]) -> PipelineContext[OutputDataT]:
        pass
