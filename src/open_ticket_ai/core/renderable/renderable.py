import typing
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class Renderable[ParamsT: BaseModel](ABC):
    def __init__(self, config: RenderableConfig, logger_factory: LoggerFactory, *_: Any, **__: Any) -> None:
        self._config: RenderableConfig = config
        self._params: ParamsT = typing.cast("ParamsT", self.get_params_model().model_validate(config.params))
        self._logger: AppLogger = logger_factory.create(config.id)

    @staticmethod
    @abstractmethod
    def get_params_model() -> type[BaseModel]:
        pass
