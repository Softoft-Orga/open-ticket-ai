import os
from logging.config import dictConfig

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.renderable import EmptyParams, RenderableConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory, _locate
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_config import OrchestratorConfig
from open_ticket_ai.core.template_rendering import JinjaRendererConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike[str] | None = None, app_config: AppConfig | None = None) -> None:
        """Initialize AppModule with optional config path.

        Args:
            config_path: Path to config.yml. If None, uses OPEN_TICKET_AI_CONFIG
                        environment variable or falls back to default location.
        """
        self.config_path = config_path
        self.app_config = app_config or AppConfig()

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        config_loader = ConfigLoader(self.app_config)
        config = config_loader.load_config(self.config_path)
        print(config.infrastructure.logging.model_dump_json(indent=4, by_alias=True, exclude_none=True))
        dictConfig(config.infrastructure.logging.model_dump(by_alias=True, exclude_none=True))
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(RenderableFactory, scope=singleton)


    @provider
    def _create_renderer_from_service(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        service_id = config.infrastructure.default_template_renderer
        service_config = next((s for s in config.services if s.id == service_id), None)
        if not service_config:
            raise ValueError(f"Template renderer service with id '{service_id}' not found")

        cls = _locate(service_config.use)
        if cls is JinjaRenderer:
            raise TypeError(f"Service '{service_id}' (class '{service_config.use}') is not JinjaRenderer")

        params = service_config.params.model_dump()
        config_obj = JinjaRendererConfig.model_validate(params)
        return cls(config_obj)  # type: ignore[abstract]

    @provider
    @singleton
    def provide_logger_factory(self, config: RawOpenTicketAIConfig) -> LoggerFactory:
        return create_logger_factory(config.infrastructure.logging)

    @provider
    def provide_orchestrator_config(self, config: RawOpenTicketAIConfig) -> OrchestratorConfig:
        return config.orchestrator

    @multiprovider
    def provide_registerable_configs(self, config: RawOpenTicketAIConfig) -> list[RenderableConfig[EmptyParams]]:
        return config.services
