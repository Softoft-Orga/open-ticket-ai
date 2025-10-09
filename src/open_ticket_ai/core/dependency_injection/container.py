import os
from logging.config import dictConfig
from pathlib import Path

from injector import Binder, Module, multiprovider, provider, singleton

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
    def __init__(self, config_path: str | os.PathLike | None = None):
        """Initialize AppModule with optional config path.

        Args:
            config_path: Path to config.yml. If None, uses OPEN_TICKET_AI_CONFIG
                        environment variable or falls back to default location.
        """
        if config_path is None:
            config_path = os.getenv("OPEN_TICKET_AI_CONFIG", Path.cwd() / "config.yml")
        self.config_path = config_path

    def configure(self, binder: Binder):
        config_loader = ConfigLoader()
        config = config_loader.load_config(self.config_path)
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