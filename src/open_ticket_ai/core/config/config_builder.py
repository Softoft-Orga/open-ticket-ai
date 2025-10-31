from __future__ import annotations

from datetime import timedelta
from typing import Any

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.config.pipe_config_builder import PipeConfigBuilder, PipeConfigFactory
from open_ticket_ai.core.injectables.injectable_models import InjectableConfigBase
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


class ConfigBuilder:
    """Fluent builder for constructing `AppConfig` instances in tests."""

    def __init__(self) -> None:
        self._logging_config = LoggingConfig(level="INFO")
        self._services: dict[str, InjectableConfigBase] = {}
        self._orchestrator: PipeConfig | None = None
        self._plugins: list[str] = []
        self._pipe_factory = PipeConfigFactory()

    def with_logging(
            self,
            level: str = "INFO",
            log_to_file: bool = False,
            log_file_path: str | None = None,
    ) -> ConfigBuilder:
        self._logging_config = LoggingConfig(
            level=level,
            log_to_file=log_to_file,
            log_file_path=log_file_path,
        )
        return self

    def add_plugin(self, plugin_name: str) -> ConfigBuilder:
        self._plugins.append(plugin_name)
        return self

    def add_service(
            self,
            service_id: str,
            use: str,
            params: dict[str, Any] | None = None,
            injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        self._services[service_id] = InjectableConfigBase(
            use=use,
            params=params or {},
            injects=injects or {},
        )
        return self

    def add_jinja_renderer(self, service_id: str = "jinja_default") -> ConfigBuilder:
        return self.add_service(
            service_id=service_id,
            use="base:JinjaRenderer",
            params={},
        )

    @property
    def pipe_factory(self) -> PipeConfigFactory:
        return self._pipe_factory

    def set_orchestrator(
            self,
            *,
            use: str = "base:SimpleSequentialOrchestrator",
            params: dict[str, Any] | None = None,
            orchestrator_id: str = "orchestrator",
            injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        params_copy = dict(params or {})
        steps_data = params_copy.pop("steps", None)
        builder = self._pipe_factory.create_composite_builder(
            orchestrator_id,
            params=params_copy,
            injects=injects,
            use=use,
        )
        if steps_data:
            builder.add_steps(
                step if isinstance(step, PipeConfig) else PipeConfig.model_validate(step)
                for step in steps_data
            )
        self._orchestrator = builder.build()
        return self

    def configure_simple_orchestrator(
            self,
            *,
            orchestrator_id: str = "orchestrator",
            orchestrator_sleep: timedelta | None = None,
    ) -> ConfigBuilder:
        params: dict[str, Any] = {}
        if orchestrator_sleep is not None:
            params["orchestrator_sleep"] = orchestrator_sleep
        return self.set_orchestrator(params=params, orchestrator_id=orchestrator_id)

    def add_orchestrator_step(
            self,
            step_id: str,
            use: str,
            params: dict[str, Any] | None = None,
            injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        pipe = self._pipe_factory.create_pipe(step_id, use, params=params, injects=injects)
        return self.add_orchestrator_pipe(pipe)

    def add_orchestrator_pipe(self, pipe: PipeConfig) -> ConfigBuilder:
        self._ensure_orchestrator()
        assert self._orchestrator is not None
        builder = self._create_orchestrator_builder(self._orchestrator)
        builder.add_step(pipe)
        self._orchestrator = builder.build()
        return self

    def build(self) -> AppConfig:
        self._ensure_services()
        self._ensure_orchestrator()
        if self._orchestrator is None:
            raise ValueError("Orchestrator must be set before building the configuration.")
        return AppConfig(
            open_ticket_ai=OpenTicketAIConfig(
                api_version=">=1.0.0",
                plugins=list(self._plugins),
                infrastructure=InfrastructureConfig(
                    logging=self._logging_config,
                ),
                services=self._services,
                orchestrator=self._orchestrator,
            )
        )

    @staticmethod
    def minimal() -> AppConfig:
        return ConfigBuilder().build()

    @staticmethod
    def with_defaults() -> ConfigBuilder:
        return ConfigBuilder().with_logging(level="DEBUG").add_jinja_renderer().configure_simple_orchestrator()

    def _ensure_services(self) -> None:
        if not self._services:
            self.add_jinja_renderer()

    def _ensure_orchestrator(self) -> None:
        if self._orchestrator is None:
            self.configure_simple_orchestrator()

    def _create_orchestrator_builder(self, orchestrator: PipeConfig) -> PipeConfigBuilder:
        params = dict(orchestrator.params)
        steps = params.pop("steps", [])
        builder = self._pipe_factory.create_composite_builder(
            orchestrator.id,
            params=params,
            injects=orchestrator.injects,
            use=orchestrator.use,
        )
        if steps:
            builder.add_steps(
                step if isinstance(step, PipeConfig) else PipeConfig.model_validate(step)
                for step in steps
            )
        return builder
