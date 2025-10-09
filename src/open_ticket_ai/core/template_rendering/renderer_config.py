from typing import Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict, TypeAdapter


class TemplateRendererEnvConfig(BaseModel):
    prefix: str | None = Field(default="OTAI_", description="Primary environment variable prefix")
    allowlist: set[str] | None = Field(default=None, description="Allowed environment variable names")
    denylist: set[str] | None = Field(default=None, description="Denied environment variable names")


class TemplateRendererConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str = Field(..., description="Type of template renderer")
    env_config: TemplateRendererEnvConfig = Field(
        default_factory=TemplateRendererEnvConfig, description="Environment variable configuration"
    )


class JinjaRendererConfig(TemplateRendererConfig):
    type: Literal["jinja"] = "jinja"
    autoescape: bool = Field(default=False, description="Enable autoescaping in Jinja2")
    trim_blocks: bool = Field(default=True, description="Trim blocks in Jinja2")
    lstrip_blocks: bool = Field(default=True, description="Left-strip blocks in Jinja2")

class MustacheRendererConfig(TemplateRendererConfig):
    type: Literal["mustache"] = "mustache"

SpecificTemplateRendererConfig = Annotated[JinjaRendererConfig | MustacheRendererConfig, Field(discriminator="type")]
