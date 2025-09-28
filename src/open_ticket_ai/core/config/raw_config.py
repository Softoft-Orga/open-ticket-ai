from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.jinja2_env import render_recursive


class RawConfig[RenderedConfig: BaseModel](BaseModel):
    def render(self, scope: dict[str, Any] | BaseModel) -> RenderedConfig:
        return render_recursive(self.model_dump(), scope)
