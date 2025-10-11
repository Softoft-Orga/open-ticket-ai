import os
from logging.config import dictConfig

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.registerable import RegisterableConfig
from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering import TemplateRendererConfig
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
)
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike | None = None, app_config: AppConfig | None = None):
        """Initialize AppModule with optional config path.

        Args:
            config_path: Path to config.yml. If None, uses OPEN_TICKET_AI_CONFIG
                        environment variable or falls back to default location.
        """
        self.config_path = config_path
        self.app_config = app_config or AppConfig()

    def configure(self, binder: Binder):
        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        config_loader = ConfigLoader(self.app_config)
        config = config_loader.load_config(self.config_path)
        print(config.general_config.logging.model_dump_json(indent=4, by_alias=True, exclude_none=True))
        dictConfig(config.general_config.logging.model_dump(by_alias=True, exclude_none=True))
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
        return config.services
