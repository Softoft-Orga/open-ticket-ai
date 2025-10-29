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
from open_ticket_ai.core.plugins.plugin_loader import PluginLoader
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, app_config: AppConfig | None = None) -> None:
        self.app_config = app_config or AppConfig()
        self.logger_factory = create_logger_factory(self.app_config.open_ticket_ai.infrastructure.logging)
        self.component_registry = ComponentRegistry()
        self.plugin_loader = PluginLoader(
            registry=self.component_registry,
            logger_factory=self.logger_factory,
            app_config=self.app_config,
        )
        self.plugin_loader.load_plugins()

    def configure(self, binder: Binder) -> None:
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        binder.bind(ComponentRegistry, to=self.component_registry, scope=singleton)
        binder.bind(PluginLoader, to=self.plugin_loader, scope=singleton)
        binder.bind(OpenTicketAIConfig, to=self.app_config.open_ticket_ai, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    @singleton
    def provide_logger_factory(self) -> LoggerFactory:
        return self.logger_factory

    @provider
    def create_renderer_from_service(
        self, config: OpenTicketAIConfig, logger_factory: LoggerFactory
    ) -> TemplateRenderer:
        logger = logger_factory.create("AppModule")
        logger.debug("🔧 Creating TemplateRenderer from service configuration")

        all_template_renderer_services = find_all_configured_services_of_type(
            config.get_services_list(),
            self.component_registry,
            TemplateRenderer,
        )

        if len(all_template_renderer_services) > 1:
            logger.error(f"❌ Multiple TemplateRenderer configurations found: {len(all_template_renderer_services)}")
            raise MultipleConfigurationsForSingletonServiceError(TemplateRenderer)

        if len(all_template_renderer_services) == 0:
            logger.error("❌ No TemplateRenderer configuration found")
            raise MissingConfigurationForRequiredServiceError(TemplateRenderer)

        service_config = all_template_renderer_services[0]
        logger.debug(f"Using TemplateRenderer service: {service_config.id}")

        cls: type[TemplateRenderer] = typing.cast(
            type[TemplateRenderer], self.component_registry.get_injectable(by_identifier=service_config.use)
        )

        renderer = cls(service_config, logger_factory=logger_factory)
        logger.info(f"✅ TemplateRenderer created: {cls.__name__}")
        return renderer
