# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

from abc import ABC, abstractmethod

from .context import PipelineContext


class Pipe(ABC):
    @abstractmethod
    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        pass
