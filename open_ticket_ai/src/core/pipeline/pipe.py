# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\pipe.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel

from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from .context import PipelineContext
from ..config.config_models import ProvidableConfig


class Pipe[ConfigT: ProvidableConfig, InputDataT: BaseModel, OutputDataT: BaseModel](Providable, ABC):
    InputModel: ClassVar[type[BaseModel]]
    OutputModel: ClassVar[type[BaseModel]]

    def __init__(self, config: ConfigT):
        super().__init__(config)
        self.config: ConfigT = config

    @abstractmethod
    def process(self, context: PipelineContext[InputDataT]) -> PipelineContext[OutputDataT]:
        pass
