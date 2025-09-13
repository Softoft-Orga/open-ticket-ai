# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel

from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from .context import PipelineContext
from ..config.config_models import ProvidableConfig


class Pipe[InputDataT: BaseModel, OutputDataT: BaseModel](Providable, ABC):
    InputDataType: type[InputDataT] = type[InputDataT]

    OutputDataType: type[OutputDataT] = type[OutputDataT]

    def __init__(self, config: ProvidableConfig):
        super().__init__(config)

    @abstractmethod
    def process(self, context: PipelineContext[InputDataT]) -> PipelineContext[OutputDataT]:
        pass
