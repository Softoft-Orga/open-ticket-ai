from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig

if TYPE_CHECKING:
    from open_ticket_ai.core.config.app_config import AppConfig

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
    default_template_renderer: str = Field(default="jinja_default")


class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=lambda: [])
    infrastructure: InfrastructureConfig = Field(default_factory=InfrastructureConfig)
    services: list[RegisterableConfig] = Field(default_factory=lambda: [])
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)


def load_config(config_path: str | os.PathLike[str], app_config: AppConfig | None = None) -> RawOpenTicketAIConfig:
    from open_ticket_ai.core.config.app_config import AppConfig as DefaultAppConfig  # noqa: PLC0415
    from open_ticket_ai.core.config.config_loader import ConfigLoader  # noqa: PLC0415

    if app_config is None:
        app_config = DefaultAppConfig()

    loader = ConfigLoader(app_config)
    return loader.load_config(config_path)
