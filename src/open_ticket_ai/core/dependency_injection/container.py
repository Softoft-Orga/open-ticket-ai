import typing

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
)
from open_ticket_ai.core.config.errors import (
    MissingConfigurationForRequiredServiceError,
    MultipleConfigurationsForSingletonServiceError,
)
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.service_registry_util import find_all_configured_services_of_type
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, app_config: AppConfig | None = None) -> None:
        self.app_config = app_config or AppConfig()
        self.component_registry = ComponentRegistry()

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        binder.bind(OpenTicketAIConfig, to=self.app_config.open_ticket_ai, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    def create_renderer_from_service(
        self, config: OpenTicketAIConfig, logger_factory: LoggerFactory
    ) -> TemplateRenderer:
        all_template_renderer_services = find_all_configured_services_of_type(
            config.get_services_list(),
            self.component_registry,
            TemplateRenderer,
        )

        if len(all_template_renderer_services) > 1:
            raise MultipleConfigurationsForSingletonServiceError(TemplateRenderer)

        if len(all_template_renderer_services) == 0:
            raise MissingConfigurationForRequiredServiceError(TemplateRenderer)
        service_config = all_template_renderer_services[0]
        cls: type[TemplateRenderer] = typing.cast(
            type[TemplateRenderer], self.component_registry.get_injectable(service_config.use)
        )
        return cls(service_config, logger_factory=logger_factory)  # type: ignore[abstract]

    @provider
    @singleton
    def provide_logger_factory(self, config: OpenTicketAIConfig) -> LoggerFactory:
        return create_logger_factory(config.infrastructure.logging)
