import os
from logging.config import dictConfig
from pathlib import Path

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.plugins.manager import PluginManager
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
    TemplateRendererEnvConfig,
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
        
        plugin_manager = PluginManager()
        plugin_manager.discover_and_load()
        binder.bind(PluginManager, to=plugin_manager, scope=singleton)
        
        plugin_manager.register_services(binder)

    @provider
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        renderer_config = config.general_config.get("template_renderer", {})
        renderer_type = renderer_config.get("type", "jinja")
        if renderer_type != "jinja":
            raise ValueError(f"Unsupported template renderer type: {renderer_type}")
        params = renderer_config.get("params", {})
        
        env_config_fields = {
            "prefix",
            "extra_prefixes",
            "allowlist",
            "denylist",
            "key",
            "provider",
            "refresh_env_on_each_render",
        }
        env_params = {}
        jinja_params = {}
        
        for k, v in params.items():
            if k.startswith("env_"):
                field_name = k.replace("env_", "")
                env_params[field_name] = v
            elif k in env_config_fields:
                env_params[k] = v
            elif k != "config":
                jinja_params[k] = v
        
        env_config = TemplateRendererEnvConfig(**env_params) if env_params else TemplateRendererEnvConfig()
        jinja_config = JinjaRendererConfig(env_config=env_config, **jinja_params)
        
        return JinjaRenderer(config=jinja_config)
