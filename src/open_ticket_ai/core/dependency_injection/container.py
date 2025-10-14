import os
import typing
from logging.config import dictConfig
from pydoc import locate

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_config import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable import RenderableConfig
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory
from open_ticket_ai.core.template_rendering import JinjaRendererConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike[str] | None = None, app_config: AppConfig | None = None) -> None:
        self.config_path = config_path
        self.app_config = app_config or AppConfig()

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        # Create a temporary logger factory for config loading
        temp_logger_factory = create_logger_factory(LoggingDictConfig())
        config_loader = ConfigLoader(self.app_config, temp_logger_factory)
        config = config_loader.load_config(self.config_path)
        print(config.infrastructure.logging.model_dump_json(indent=4, by_alias=True, exclude_none=True))
        dictConfig(config.infrastructure.logging.model_dump(by_alias=True, exclude_none=True))
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(RenderableFactory, scope=singleton)

    @provider
    def _create_renderer_from_service(
        self, config: RawOpenTicketAIConfig, logger_factory: LoggerFactory
    ) -> TemplateRenderer:
        service_id = config.infrastructure.default_template_renderer
        service_config = next((s for s in config.services if s.id == service_id), None)
        if not service_config:
            raise ValueError(f"Template renderer service with id '{service_id}' not found")

        cls: type = typing.cast(type, locate(service_config.use))
        config_obj = JinjaRendererConfig.model_validate(service_config.params)
        return cls(config_obj, logger_factory=logger_factory)  # type: ignore[abstract]

    @provider
    @singleton
    def provide_logger_factory(self, config: RawOpenTicketAIConfig) -> LoggerFactory:
        return create_logger_factory(config.infrastructure.logging)

    @provider
    def provide_orchestrator_config(self, config: RawOpenTicketAIConfig) -> OrchestratorConfig:
        return config.orchestrator

    @multiprovider
    def provide_registerable_configs(self, config: RawOpenTicketAIConfig) -> list[RenderableConfig]:
        return config.services
