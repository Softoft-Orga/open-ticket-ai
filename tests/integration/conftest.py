# tests/integration/conftest.py
"""Integration test fixtures providing real instances of core components."""

import pytest
from injector import Injector

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_builder import ConfigBuilder
from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig, InjectableConfigBase
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig, LoggingFormatConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
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
        format=LoggingFormatConfig(
            message_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", date_format="%Y-%m-%d %H:%M:%S"
        ),
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


@pytest.fixture
def integration_config_builder() -> ConfigBuilder:
    """ConfigBuilder for integration tests."""
    return ConfigBuilder.with_defaults()
