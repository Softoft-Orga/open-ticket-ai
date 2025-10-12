import os
from logging.config import dictConfig

from injector import Binder, Module, multiprovider, provider, singleton

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
)
from open_ticket_ai.core.config.renderable import RenderableConfig
from open_ticket_ai.core.config.registerable_factory import RegisterableFactory
from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig
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
        from typing import cast  # noqa: PLC0415

        binder.bind(AppConfig, to=self.app_config, scope=singleton)
        config_loader = ConfigLoader(self.app_config)
        config = config_loader.load_config(cast(os.PathLike[str], self.config_path))
        print(config.infrastructure.logging.model_dump_json(indent=4, by_alias=True, exclude_none=True))
        dictConfig(config.infrastructure.logging.model_dump(by_alias=True, exclude_none=True))
        binder.bind(RawOpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(RegisterableFactory, scope=singleton)

    @provider
    def provide_template_renderer(self, config: RawOpenTicketAIConfig) -> TemplateRenderer:
        from pydoc import locate  # noqa: PLC0415
        from typing import cast  # noqa: PLC0415

        template_renderer_id = config.infrastructure.default_template_renderer

        renderer_service_config = None
        for service_config in config.services:
            if service_config.id == template_renderer_id:
                renderer_service_config = service_config
                break

        if renderer_service_config is None:
            raise ValueError(
                f"Template renderer service with id '{template_renderer_id}' "
                f"not found in services. Available services: "
                f"{[s.id for s in config.services]}"
            )

        use_str = renderer_service_config.use
        if ":" in use_str:
            m, c = use_str.split(":", 1)
            use_str = f"{m}.{c}"

        renderer_class = locate(use_str)
        if renderer_class is None:
            raise ValueError(f"Cannot locate template renderer class '{renderer_service_config.use}'")

        renderer_class_typed = cast(type, renderer_class)
        if not issubclass(renderer_class_typed, TemplateRenderer):
            raise TypeError(f"Class '{renderer_service_config.use}' is not a TemplateRenderer subclass")

        params = renderer_service_config.model_dump().get("params", {})
        config_class_name = renderer_class_typed.__name__ + "Config"
        config_module = renderer_class_typed.__module__.rsplit(".", 1)[0] + ".renderer_config"

        config_module_obj = locate(config_module)
        if config_module_obj is None:
            raise ValueError(f"Cannot locate config module '{config_module}'")

        config_class = getattr(config_module_obj, config_class_name, None)
        if config_class is None:
            raise ValueError(f"Cannot find config class '{config_class_name}' in module '{config_module}'")

        renderer_config = config_class(**params)
        return renderer_class_typed(config=renderer_config)  # type: ignore[call-arg]

    @provider
    def provide_orchestrator_config(self, config: RawOpenTicketAIConfig) -> OrchestratorConfig:
        return config.orchestrator

    @multiprovider
    def provide_registerable_configs(self, config: RawOpenTicketAIConfig) -> list[RenderableConfig]:
        return config.services
