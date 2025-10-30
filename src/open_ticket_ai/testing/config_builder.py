from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
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
        if plugin_name not in self._plugins:
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

    def set_orchestrator(
        self,
        *,
        use: str = "base:SimpleSequentialOrchestrator",
        params: dict[str, Any] | None = None,
        orchestrator_id: str = "orchestrator",
        injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        self._orchestrator = PipeConfig(
            id=orchestrator_id,
            use=use,
            params=params or {},
            injects=injects or {},
        )
        return self

    def configure_simple_orchestrator(
        self,
        *,
        orchestrator_id: str = "orchestrator",
        orchestrator_sleep: str | None = None,
    ) -> ConfigBuilder:
        params: dict[str, Any] = {}
        if orchestrator_sleep is not None:
            params["orchestrator_sleep"] = orchestrator_sleep
        return self.set_orchestrator(
            use="base:SimpleSequentialOrchestrator",
            params=params,
            orchestrator_id=orchestrator_id,
        )

    def add_orchestrator_step(
        self,
        step_id: str,
        use: str,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        pipe = ConfigBuilder.pipe(step_id, use, params=params, injects=injects)
        return self.add_orchestrator_pipe(pipe)

    def add_orchestrator_pipe(self, pipe: PipeConfig) -> ConfigBuilder:
        self._ensure_orchestrator()
        assert self._orchestrator is not None
        current_params = dict(self._orchestrator.params)
        steps = list(current_params.get("steps", []))
        steps.append(pipe.model_dump(mode="json", exclude_none=True))
        current_params["steps"] = steps
        self._orchestrator = self._orchestrator.model_copy(update={"params": current_params})
        return self

    def build(self) -> AppConfig:
        self._ensure_services()
        self._ensure_orchestrator()
        assert self._orchestrator is not None
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

    @staticmethod
    def pipe(
        pipe_id: str,
        use: str,
        *,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use=use,
            params=params or {},
            injects=injects or {},
        )

    @staticmethod
    def composite_pipe(
        pipe_id: str,
        steps: Sequence[PipeConfig],
        *,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
        use: str = "base:CompositePipe",
    ) -> PipeConfig:
        combined_params = dict(params or {})
        combined_params["steps"] = [step.model_dump(mode="json", exclude_none=True) for step in steps]
        return ConfigBuilder.pipe(pipe_id, use, params=combined_params, injects=injects)

    @staticmethod
    def interval_trigger(
        *,
        trigger_id: str = "interval_trigger",
        interval: str = "PT5S",
        params: dict[str, Any] | None = None,
    ) -> PipeConfig:
        trigger_params = dict(params or {})
        trigger_params.setdefault("interval", interval)
        return ConfigBuilder.pipe(trigger_id, "base:IntervalTrigger", params=trigger_params)

    @staticmethod
    def simple_sequential_runner(
        *,
        runner_id: str,
        on: PipeConfig,
        run: PipeConfig,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> PipeConfig:
        runner_params = dict(params or {})
        runner_params["on"] = on.model_dump(mode="json", exclude_none=True)
        runner_params["run"] = run.model_dump(mode="json", exclude_none=True)
        return ConfigBuilder.pipe(
            runner_id,
            "base:SimpleSequentialRunner",
            params=runner_params,
            injects=injects,
        )

    def _ensure_services(self) -> None:
        if not self._services:
            self.add_jinja_renderer()

    def _ensure_orchestrator(self) -> None:
        if self._orchestrator is None:
            self.configure_simple_orchestrator()
