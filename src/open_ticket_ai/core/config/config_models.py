from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.orchestration.orchestrator_config import OrchestratorConfig
from open_ticket_ai.core.template_rendering import JinjaRendererConfig

LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class FormatterConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    class_: str | None = Field(default=None, alias="class")
    format: str | None = None
    datefmt: str | None = None
    style: Literal["%", "{", "$"] | None = None
    call: str | None = Field(default=None, alias="()")


class FilterConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    class_: str | None = Field(default=None, alias="class")
    name: str | None = None
    call: str | None = Field(default=None, alias="()")


class HandlerConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    class_: str = Field(alias="class")
    level: LogLevel | None = None
    formatter: str | None = None
    filters: list[str] | None = None
    call: str | None = Field(default=None, alias="()")


class LoggerConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    level: LogLevel | None = None
    handlers: list[str] | None = None
    propagate: bool | None = None
    filters: list[str] | None = None


class RootConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    level: LogLevel | None = None
    handlers: list[str] | None = None
    filters: list[str] | None = None


class LoggingDictConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    version: Literal[1] = 1
    disable_existing_loggers: bool | None = None
    incremental: bool | None = None
    root: RootConfig | None = None
    loggers: dict[str, LoggerConfig] = Field(default_factory=lambda: {})
    handlers: dict[str, HandlerConfig] = Field(default_factory=lambda: {})
    formatters: dict[str, FormatterConfig] = Field(default_factory=lambda: {})
    filters: dict[str, FilterConfig] = Field(default_factory=lambda: {})


class InfrastructureConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    logging: LoggingDictConfig = Field(default_factory=LoggingDictConfig)
    template_renderer_config: JinjaRendererConfig = Field(
        default_factory=JinjaRendererConfig,
        description="(Deprecated) in future versions will be set through the services section",
    )


class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=lambda: [])
    infrastructure: InfrastructureConfig = Field(default_factory=InfrastructureConfig)
    services: list[RenderableConfig[Any]] = Field(default_factory=lambda: [])
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
