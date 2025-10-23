# tests/integration/conftest.py
"""Integration test fixtures providing real instances of core components."""

from typing import Any

import pytest
from injector import Injector
from otai_base.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig, InjectableConfigBase
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from tests.mocked_ticket_system import MockedTicketSystem

# Mark all tests in this directory as integration tests
pytestmark = [pytest.mark.integration]


# ============================================================================
# BASIC INFRASTRUCTURE FIXTURES
# ============================================================================


@pytest.fixture
def integration_logging_config() -> LoggingConfig:
    """LoggingConfig for integration tests with DEBUG level."""
    return LoggingConfig(
        level="DEBUG",
        log_to_file=False,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        date_format="%Y-%m-%d %H:%M:%S",
    )


@pytest.fixture
def integration_logger_factory(integration_logging_config: LoggingConfig) -> LoggerFactory:
    """Real LoggerFactory instance for integration tests."""
    return create_logger_factory(integration_logging_config)


@pytest.fixture
def integration_component_registry() -> ComponentRegistry:
    """Real ComponentRegistry with otai_base plugin registered."""
    registry = ComponentRegistry()

    # Import and register otai_base plugin components
    from otai_base.base_plugin import BasePlugin

    # Create minimal app config for plugin initialization
    minimal_config = AppConfig(
        open_ticket_ai=OpenTicketAIConfig(
            infrastructure=InfrastructureConfig(logging=LoggingConfig()),
            services={
                "jinja_default": InjectableConfigBase(
                    use="base:JinjaRenderer",
                )
            },
        )
    )

    # Load otai_base plugin
    plugin = BasePlugin(minimal_config)
    plugin.on_load(registry)

    return registry


# ============================================================================
# CONFIGURATION FIXTURES
# ============================================================================


@pytest.fixture
def integration_infrastructure_config(integration_logging_config: LoggingConfig) -> InfrastructureConfig:
    """InfrastructureConfig for integration tests."""
    return InfrastructureConfig(
        logging=integration_logging_config,
    )


@pytest.fixture
def integration_jinja_service_config() -> InjectableConfig:
    """Service config for JinjaRenderer."""
    return InjectableConfig(
        id="jinja_renderer",
        use="base:JinjaRenderer",
        params={},
    )


@pytest.fixture
def integration_app_config(
    integration_infrastructure_config: InfrastructureConfig,
    integration_jinja_service_config: InjectableConfig,
) -> AppConfig:
    """Complete AppConfig for integration tests."""
    return AppConfig(
        open_ticket_ai=OpenTicketAIConfig(
            infrastructure=integration_infrastructure_config,
            services={
                integration_jinja_service_config.id: InjectableConfigBase.model_validate(
                    integration_jinja_service_config.model_dump(exclude={"id"})
                )
            },
        )
    )


# ============================================================================
# DEPENDENCY INJECTION FIXTURES
# ============================================================================


@pytest.fixture
def integration_app_module(integration_app_config: AppConfig) -> AppModule:
    """Real AppModule with full DI container setup."""
    return AppModule(integration_app_config)


@pytest.fixture
def integration_injector(integration_app_module: AppModule) -> Injector:
    """Real Injector with AppModule configured."""
    return Injector([integration_app_module])


# ============================================================================
# TEMPLATE RENDERING FIXTURES
# ============================================================================


@pytest.fixture
def integration_template_renderer(integration_injector: Injector) -> TemplateRenderer:
    """Real TemplateRenderer instance from DI container."""
    return integration_injector.get(TemplateRenderer)


@pytest.fixture
def integration_rendering_context() -> PipeContext:
    """Sample PipeContext for template rendering tests."""
    return PipeContext(
        pipe_results={
            "fetch_tickets": {
                "succeeded": True,
                "data": {
                    "fetched_tickets": [
                        {"id": "T-1", "subject": "Test ticket", "queue": {"name": "Support"}},
                    ],
                    "count": 1,
                },
            },
            "classify_queue": {
                "succeeded": True,
                "data": {
                    "label": "billing",
                    "confidence": 0.95,
                },
            },
        },
        params={
            "threshold": 0.8,
            "model_name": "test-model",
        },
    )


# ============================================================================
# PIPELINE FIXTURES
# ============================================================================


@pytest.fixture
def integration_pipe_factory(integration_injector: Injector) -> PipeFactory:
    """Real PipeFactory instance from DI container."""
    return integration_injector.get(PipeFactory)


@pytest.fixture
def integration_empty_pipe_context() -> PipeContext:
    """Empty PipeContext for pipeline execution."""
    return PipeContext.empty()


# ============================================================================
# TICKET SYSTEM FIXTURES
# ============================================================================


@pytest.fixture
def integration_mocked_ticket_system(integration_logger_factory: LoggerFactory) -> MockedTicketSystem:
    """MockedTicketSystem with pre-populated test data for integration tests."""
    config = InjectableConfig(id="test_ticket_system", use="test:MockedTicketSystem")
    system = MockedTicketSystem(config=config, logger_factory=integration_logger_factory)

    # Add test tickets
    system.add_test_ticket(
        id="TICKET-INT-001",
        subject="Integration test ticket 1",
        body="This is a test ticket for integration testing",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        notes=[],
    )

    system.add_test_ticket(
        id="TICKET-INT-002",
        subject="Integration test ticket 2",
        body="Another test ticket with high priority",
        queue=UnifiedEntity(id="2", name="Development"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[
            UnifiedNote(id="NOTE-1", subject="Test note", body="This is a test note"),
        ],
    )

    system.add_test_ticket(
        id="TICKET-INT-003",
        subject="Urgent integration issue",
        body="Requires immediate attention for integration testing",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[],
    )

    return system


class ConfigBuilder:
    """
    Fluent builder for AppConfig instances in integration tests.

    Example usage:
        config = (ConfigBuilder()
            .with_logging(level="DEBUG")
            .add_service("jinja", "base:JinjaRenderer")
            .set_orchestrator("base:SimpleSequentialOrchestrator")
            .build())
    """

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
        """Configure logging settings."""
        self._logging_config = LoggingConfig(
            level=level,
            log_to_file=log_to_file,
            log_file_path=log_file_path,
        )
        return self

    def add_plugin(self, plugin_name: str) -> ConfigBuilder:
        """Add a plugin to load."""
        self._plugins.append(plugin_name)
        return self

    def add_service(
        self,
        service_id: str,
        use: str,
        params: dict[str, Any] | None = None,
        injects: dict[str, str] | None = None,
    ) -> ConfigBuilder:
        """Add a service configuration."""
        self._services[service_id] = InjectableConfigBase(
            use=use,
            params=params or {},
            injects=injects or {},
        )
        return self

    def add_jinja_renderer(self, service_id: str = "jinja_default") -> ConfigBuilder:
        """Add default JinjaRenderer service."""
        return self.add_service(
            service_id=service_id,
            use="base:JinjaRenderer",
            params={},
        )

    def set_orchestrator(
        self,
        use: str = "base:SimpleSequentialOrchestrator",
        params: dict[str, Any] | None = None,
    ) -> ConfigBuilder:
        """Configure the orchestrator."""
        self._orchestrator = PipeConfig(
            id="orchestrator",
            use=use,
            params=params or {},
        )
        return self

    def add_orchestrator_step(
        self,
        step_id: str,
        use: str,
        params: dict[str, Any] | None = None,
    ) -> ConfigBuilder:
        """Add a step to the orchestrator configuration."""
        if self._orchestrator is None:
            self.set_orchestrator()

        steps = list(self._orchestrator.params.get("steps", []))
        steps.append(
            {
                "id": step_id,
                "use": use,
                "params": params or {},
            }
        )

        self._orchestrator = self._orchestrator.model_copy(
            update={"params": {**self._orchestrator.params, "steps": steps}}
        )
        return self

    def build(self) -> AppConfig:
        """Build the final AppConfig instance."""
        # Ensure required services exist
        if not self._services:
            self.add_jinja_renderer()

        # Ensure orchestrator exists
        if self._orchestrator is None:
            self.set_orchestrator()

        return AppConfig(
            open_ticket_ai=OpenTicketAIConfig(
                api_version="1",
                plugins=self._plugins,
                infrastructure=InfrastructureConfig(
                    logging=self._logging_config,
                ),
                services=self._services,
                orchestrator=self._orchestrator,
            )
        )

    @staticmethod
    def minimal() -> AppConfig:
        """Create minimal valid AppConfig."""
        return ConfigBuilder().build()

    @staticmethod
    def with_defaults() -> ConfigBuilder:
        """Create builder with common defaults."""
        return ConfigBuilder().with_logging(level="DEBUG").add_jinja_renderer().set_orchestrator()


@pytest.fixture
def integration_config_builder() -> ConfigBuilder:
    """ConfigBuilder for integration tests."""
    return ConfigBuilder.with_defaults()
