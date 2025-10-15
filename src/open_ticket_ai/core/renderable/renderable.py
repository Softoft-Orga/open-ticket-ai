from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.logging.logging_iface import LoggerFactory, AppLogger
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class Renderable[ParamsT: StrictBaseModel](ABC):
    def __init__(self, config: RenderableConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        self._config: RenderableConfig = config
        self._params: ParamsT = self.get_params_model().model_validate(config.params)
        self._logger: AppLogger = logger_factory.create(config.id)

    @staticmethod
    @abstractmethod
    def get_params_model() -> type[StrictBaseModel]:
        pass
