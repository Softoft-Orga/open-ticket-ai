import typing
from pydoc import locate

from injector import Binder, Module, provider, singleton

from open_ticket_ai.base.loggers.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
)
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering import JinjaRendererConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, app_config: AppConfig | None = None) -> None:
        self.app_config = app_config or AppConfig()

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        binder.bind(OpenTicketAIConfig, to=self.app_config.open_ticket_ai, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    def create_renderer_from_service(
            self, config: OpenTicketAIConfig, logger_factory: LoggerFactory
    ) -> TemplateRenderer:
        service_id = config.infrastructure.default_template_renderer
        service_config = next((s for s in config.services if s.id == service_id), None)
        if not service_config:
            raise ValueError(f"Template renderer service with id '{service_id}' not found")

        cls: type = typing.cast("type", locate(service_config.use))
        config_obj = JinjaRendererConfig.model_validate(service_config.params)
        return cls(config_obj, logger_factory=logger_factory)  # type: ignore[abstract]

    @provider
    @singleton
    def provide_logger_factory(self, config: OpenTicketAIConfig) -> LoggerFactory:
        return create_logger_factory(config.infrastructure.logging)
