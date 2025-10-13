import os
from logging.config import dictConfig

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.renderable import EmptyParams, RenderableConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory, _locate
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
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        # If default_template_renderer is specified, look up the service and instantiate it
        if config.infrastructure.default_template_renderer:
            service_id = config.infrastructure.default_template_renderer
            service_config = next((s for s in config.services if s.id == service_id), None)
            if not service_config:
                raise ValueError(f"Template renderer service with id '{service_id}' not found")

            # Import and check the class
            cls = _locate(service_config.use)
            if not issubclass(cls, TemplateRenderer):
                raise TypeError(
                    f"Service '{service_id}' (class '{service_config.use}') is not a TemplateRenderer subclass"
                )

            # For JinjaRenderer, we need to convert params to JinjaRendererConfig
            if cls == JinjaRenderer:
                if isinstance(service_config.params, dict):
                    renderer_config = JinjaRendererConfig.model_validate(service_config.params)
                else:
                    renderer_config = JinjaRendererConfig.model_validate(service_config.params.model_dump())
                return cls(renderer_config)  # type: ignore[abstract]

            # For other renderers, pass params directly
            return cls(service_config.params)  # type: ignore[abstract]

        # Fallback to legacy template_renderer_config
        template_renderer_config = config.infrastructure.template_renderer_config
        if template_renderer_config.type == "jinja":
            jinja_renderer_config = JinjaRendererConfig.model_validate(template_renderer_config.model_dump())
            return JinjaRenderer(jinja_renderer_config)
        raise ValueError(f"Unsupported template renderer type: {template_renderer_config.type}")

    @provider
    def provide_orchestrator_config(self, config: RawOpenTicketAIConfig) -> OrchestratorConfig:
        return config.orchestrator

    @multiprovider
    def provide_registerable_configs(self, config: RawOpenTicketAIConfig) -> list[RenderableConfig[EmptyParams]]:
        return config.services
