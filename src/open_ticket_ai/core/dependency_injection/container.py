import os
from logging.config import dictConfig
from pathlib import Path

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline import OrchestratorConfig
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering import TemplateRendererConfig
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
)
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike | None = None, app_config: AppConfig | None = None):
        """Initialize AppModule with optional config path and app config.

        Args:
            config_path: Path to config.yml. If None, uses environment variable
                        specified in app_config or falls back to default location.
            app_config: AppConfig instance. If None, uses default AppConfig.
        """
        if app_config is None:
            app_config = AppConfig()
        self.app_config = app_config

        if config_path is None:
            config_path = os.getenv(app_config.config_env_var, app_config.get_default_config_path())
        self.config_path = config_path

    def configure(self, binder: Binder):
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        config_loader = ConfigLoader(self.app_config, self.config_path)
        config = config_loader.load_config()
        dictConfig(config.general_config.logging)
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        renderer_config: TemplateRendererConfig = config.general_config.template_renderer
        if renderer_config.type != "jinja":
            raise ValueError(f"Unsupported template renderer type: {renderer_config.type}")

        jinja_config = JinjaRendererConfig.model_validate(renderer_config.model_dump())
        return JinjaRenderer(config=jinja_config)

    @provider
    def provide_orchestrator_config(self, config: RawOpenTicketAIConfig) -> OrchestratorConfig:
        return config.orchestrator

    @multiprovider
    def provide_registerable_configs(self, config: RawOpenTicketAIConfig) -> list[RegisterableConfig]:
        return config.defs