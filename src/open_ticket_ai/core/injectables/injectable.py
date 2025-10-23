from typing import Any, ClassVar, cast

from pydantic import BaseModel

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory


class Injectable[ParamsT: BaseModel = StrictBaseModel]:
    ParamsModel: ClassVar[type[BaseModel]] = StrictBaseModel

    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory, *_: Any, **__: Any) -> None:
        self._config: InjectableConfig = config
        self._logger: AppLogger = logger_factory.create(config.id)
        self._logger.debug(f"Initializing injectable: {self.__class__.__name__} with config: {config.model_dump()}")
        params = self.ParamsModel.model_validate(config.params)
        self._params: ParamsT = cast(ParamsT, params)

    @classmethod
    def get_registry_name(cls) -> str:
        return cls.__name__
