from typing import Annotated, Literal

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel


class TemplateRendererConfig(StrictBaseModel):
    type: str = Field(description="Type identifier for the template renderer implementation to use.")


class JinjaRendererConfig(TemplateRendererConfig):
    type: Literal["jinja"] = Field(default="jinja", description="Type identifier for Jinja2 template renderer.")


class MustacheRendererConfig(TemplateRendererConfig):
    type: Literal["mustache"] = Field(default="mustache", description="Type identifier for Mustache template renderer.")


SpecificTemplateRendererConfig = Annotated[JinjaRendererConfig | MustacheRendererConfig, Field(discriminator="type")]
