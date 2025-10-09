from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline import OrchestratorConfig
from open_ticket_ai.core.template_rendering import JinjaRendererConfig, TemplateRendererConfig
from open_ticket_ai.core.template_rendering.renderer_config import SpecificTemplateRendererConfig

LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class FormatterConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    class_: str | None = Field(default=None, alias="class")
    format: str | None = None
    datefmt: str | None = None
    style: Literal["%", "{", "$"] | None = None
    validate: bool | None = None
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

class GeneralConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    logging: LoggingDictConfig = Field(default_factory=LoggingDictConfig)
    # noinspection PyTypeHints
    template_renderer: SpecificTemplateRendererConfig = Field(default_factory=JinjaRendererConfig)

class RawOpenTicketAIConfig(BaseModel):
    plugins: list[str] = Field(default_factory=lambda: [])
    general_config: GeneralConfig = Field(default_factory=GeneralConfig)
    defs: list[RegisterableConfig] = Field(default_factory=lambda: [])
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)


def load_config(path: str | Path, app_config: AppConfig | None = None) -> RawOpenTicketAIConfig:
    if app_config is None:
        app_config = AppConfig()

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if app_config.config_yaml_root_key not in data:
        raise ValueError(f"Config file must have '{app_config.config_yaml_root_key}' as root key")
    return RawOpenTicketAIConfig(**data[app_config.config_yaml_root_key])
