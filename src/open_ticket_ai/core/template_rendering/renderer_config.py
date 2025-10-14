from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class TemplateRendererConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str = Field(..., description="Type of template renderer")


class JinjaRendererConfig(TemplateRendererConfig):
    type: Literal["jinja"] = "jinja"


class MustacheRendererConfig(TemplateRendererConfig):
    type: Literal["mustache"] = "mustache"


SpecificTemplateRendererConfig = Annotated[JinjaRendererConfig | MustacheRendererConfig, Field(discriminator="type")]
