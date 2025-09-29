import uuid

from pydantic import ImportString

from open_ticket_ai.core.config.raw_config import RenderableConfig, RawConfig, RenderedConfig


class RawRegisterableConfig(RawConfig):
    id: str | None = None
    use: ImportString | None = None


class RenderedRegistrableConfig(RenderedConfig):
    id: str = uuid.uuid4().hex
    use: str = "DefaultPipe"


class RegisterableConfig[RawConfigT: RawRegisterableConfig, RenderedConfigT: RenderedRegistrableConfig](
    RenderableConfig[RawConfigT, RenderedConfigT]
):
    pass


class RegisterableClass[RawConfigT: RawRegisterableConfig, RenderedConfigT: RenderedRegistrableConfig]:
    def __init__(self, config: RenderableConfig[RawConfigT, RenderedConfigT], *args, **kwargs):
        self._config = config

    @property
    def config(self) -> RenderedConfigT:
        return self._config.get_rendered()

    @property
    def raw_config(self) -> RawConfigT:
        return self._config.raw_config
