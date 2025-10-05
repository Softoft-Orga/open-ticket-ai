import os
from typing import Callable, Mapping

from pydantic import BaseModel, Field
from jinja2.sandbox import SandboxedEnvironment


class TemplateRendererEnvConfig(BaseModel):
    prefix: str = Field(default="OTAI_", description="Primary environment variable prefix")
    extra_prefixes: tuple[str, ...] = Field(default=(), description="Additional environment variable prefixes")
    allowlist: set[str] | None = Field(default=None, description="Allowed environment variable names")
    denylist: set[str] | None = Field(default=None, description="Denied environment variable names")
    key: str = Field(default="env", description="Template key for environment variables")
    provider: Callable[[], Mapping[str, str]] | None = Field(
        default=None, 
        description="Custom environment provider function",
        exclude=True
    )
    refresh_on_each_render: bool = Field(
        default=False, 
        description="Whether to refresh environment variables on each render"
    )


class TemplateRendererConfig(BaseModel):
    env_config: TemplateRendererEnvConfig = Field(
        default_factory=TemplateRendererEnvConfig,
        description="Environment variable configuration"
    )


class JinjaRendererConfig(TemplateRendererConfig):
    env: SandboxedEnvironment | None = Field(
        default=None, 
        description="Custom Jinja2 SandboxedEnvironment instance",
        exclude=True
    )
    autoescape: bool = Field(default=False, description="Enable autoescaping in Jinja2")
    trim_blocks: bool = Field(default=True, description="Trim blocks in Jinja2")
    lstrip_blocks: bool = Field(default=True, description="Left-strip blocks in Jinja2")
