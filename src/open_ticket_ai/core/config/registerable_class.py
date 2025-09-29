from typing import TypeVar

from pydantic import BaseModel

from open_ticket_ai.core.config.raw_config import RawRegisterableConfig, RenderedRegistrableConfig, \
    RenderableConfig

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class RegisterableClass[RawConfigT: RawRegisterableConfig, RenderedConfigT: RenderedRegistrableConfig]:
    def __init__(self, config: RenderableConfig[RawConfigT, RenderedConfigT], *args, **kwargs):
        self._config = config

    @property
    def config(self) -> RenderedConfigT:
        return self._config.get_rendered()

    @property
    def raw_config(self) -> RawConfigT:
        return self._config.raw_config
