import uuid
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.jinja2_env import render_recursive


class BaseConfig(BaseModel):
    pass


class RawConfig(BaseConfig):
    pass


class RenderedConfig(BaseConfig):
    pass


class RenderableConfig[RawConfigT: RawConfig, RenderedConfigT: RenderedConfig]:
    def __init__(self, raw_config: RawConfigT):
        self.raw_config = raw_config
        self.rendered_config: RenderedConfigT | None = None

    def render(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:
        return render_recursive(self.raw_config.model_dump(), scope)

    def save_rendered(self, scope: dict[str, Any] | BaseModel) -> RenderedConfigT:
        rendered_config = self.render(scope)
        self.rendered_config = rendered_config
        return self.rendered_config

    def get_rendered(self) -> RenderedConfigT:
        if self.rendered_config is None:
            raise ValueError("Rendered config not available. Call save_rendered first.")
        return self.rendered_config


class BaseRegisterableConfig(BaseConfig):
    id: str | None = None
    use: str | None = None
    services: dict[str, str] | str | None = None


class RenderedRegistrableConfig(BaseRegisterableConfig):
    id: str = uuid.uuid4().hex
    use: str = "DefaultPipe"
    services: dict[str, str] = {}


class RawRegisterableConfig(BaseRegisterableConfig):
    pass


class RegisterableConfig[RawConfigT: RawRegisterableConfig, RenderedConfigT: RenderedRegistrableConfig](
    RenderableConfig[RawConfigT, RenderedConfigT]
):
    pass
