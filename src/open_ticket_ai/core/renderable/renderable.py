from abc import ABC, abstractmethod

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig


class Renderable(ABC):
    def __init__(
            self, config: RenderableConfig, logger_factory: LoggerFactory, *args: object, **kwargs: object
    ) -> None:
        self._config = config
        self._params = self.get_params_model().model_validate(config.params)
        self._logger = logger_factory.create(config.id)

    @staticmethod
    @abstractmethod
    def get_params_model() -> type[BaseModel]:
        pass
