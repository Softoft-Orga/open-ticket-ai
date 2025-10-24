import typing
from typing import Any, ClassVar

from pydantic import BaseModel

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory


class Injectable[ParamsT: BaseModel = StrictBaseModel]:
    ParamsModel: ClassVar[type[BaseModel]] = StrictBaseModel

    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory, *_: Any, **__: Any) -> None:
        self._config: InjectableConfig = config
        self._logger: AppLogger = logger_factory.create(name=f"{self.__class__.__name__}.{self._config.id}")
        # noinspection PyUnnecessaryCast
        self._params: ParamsT = typing.cast(ParamsT, self.ParamsModel.model_validate(config.params))
        self._log_init()

    def _log_init(self) -> None:
        self._logger.info(f"Initializing with config: {self._config.model_dump()}")

    @classmethod
    def get_registry_name(cls) -> str:
        return cls.__name__
