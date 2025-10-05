import os
from logging.config import dictConfig
from pathlib import Path

from injector import Binder, Module, singleton, provider

from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
    TemplateRendererEnvConfig,
)


class AppModule(Module):
    def __init__(self, config_path: str | os.PathLike | None = None):
        """Initialize AppModule with optional config path.
        
        Args:
            config_path: Path to config.yml. If None, uses OPEN_TICKET_AI_CONFIG
                        environment variable or falls back to default location.
        """
        if config_path is None:
            config_path = os.getenv(
                "OPEN_TICKET_AI_CONFIG",
                Path.cwd() / "config.yml"
            )
        self.config_path = config_path

    def configure(self, binder: Binder):
        config_loader = ConfigLoader(self.config_path)
        config = config_loader.load_config()
        dictConfig(config.general_config["logging"])
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        renderer_config = config.general_config.get("template_renderer", {})
        renderer_type = renderer_config.get("type", "jinja")
        if renderer_type != "jinja":
            raise ValueError(f"Unsupported template renderer type: {renderer_type}")
        params = renderer_config.get("params", {})
        
        env_params = {k.replace("env_", ""): v for k, v in params.items() if k.startswith("env_")}
        jinja_params = {k: v for k, v in params.items() if not k.startswith("env_") and k != "config"}
        
        env_config = TemplateRendererEnvConfig(**env_params) if env_params else TemplateRendererEnvConfig()
        jinja_config = JinjaRendererConfig(env_config=env_config, **jinja_params)
        
        return JinjaRenderer(config=jinja_config)
