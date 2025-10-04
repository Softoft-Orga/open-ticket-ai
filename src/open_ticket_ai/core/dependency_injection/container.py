import os

from injector import Binder, Module, singleton, provider

from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
    load_config,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.util.path_util import find_python_code_root_path


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
                find_python_code_root_path() / "config.yml"
            )
        self.config_path = config_path

    def configure(self, binder: Binder):
        config = load_config(self.config_path)
        registry = UnifiedRegistry.get_registry_instance()
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(UnifiedRegistry, to=registry, scope=singleton)
        binder.bind(PipeFactory, scope=singleton)

    @provider
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        renderer_config = config.general_config.get("template_renderer", {})
        renderer_type = renderer_config.get("type", "jinja")
        if renderer_type != "jinja":
            raise ValueError(f"Unsupported template renderer type: {renderer_type}")
        params = renderer_config.get("params", {})
        return JinjaRenderer(**params)
