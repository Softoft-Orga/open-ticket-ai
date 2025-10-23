# tests/integration/conftest.py
"""
Integration test fixtures providing real instances of core components.

These fixtures wire together actual implementations (not mocks) to test
component interactions and integration points.
"""

from pathlib import Path
from typing import Any

import pytest
from injector import Injector

from open_ticket_ai.base.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
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
def integration_component_registry(integration_logger_factory: LoggerFactory) -> ComponentRegistry:
    """Real ComponentRegistry with base plugin registered."""
    registry = ComponentRegistry()

    # Import and register base plugin components
    from open_ticket_ai.base.plugin import BasePlugin

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

    # Load base plugin
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


@pytest.fixture
def integration_pipe_context_with_results() -> PipeContext:
    """PipeContext pre-populated with some pipe results."""
    return PipeContext(
        pipe_results={
            "step1": {
                "succeeded": True,
                "data": {"value": "result1"},
            },
            "step2": {
                "succeeded": True,
                "data": {"value": "result2"},
            },
        },
        params={"global_param": "test_value"},
    )


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
def integration_ticket_system_service_config(integration_mocked_ticket_system: MockedTicketSystem) -> InjectableConfig:
    """Service config for MockedTicketSystem."""
    return InjectableConfig(
        id="test_ticket_system",
        use="test:MockedTicketSystem",
        params={},
    )


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================


@pytest.fixture
def integration_sample_tickets_data() -> list[dict[str, Any]]:
    """Sample ticket data for integration tests."""
    return [
        {
            "id": "SAMPLE-001",
            "subject": "Email not working",
            "body": "User reports email delivery failures",
            "queue": {"id": "1", "name": "Support"},
            "priority": {"id": "3", "name": "Medium"},
        },
        {
            "id": "SAMPLE-002",
            "subject": "Feature request: Dark mode",
            "body": "Users requesting dark mode for better accessibility",
            "queue": {"id": "2", "name": "Development"},
            "priority": {"id": "2", "name": "Low"},
        },
        {
            "id": "SAMPLE-003",
            "subject": "URGENT: Production down",
            "body": "Critical production outage affecting all users",
            "queue": {"id": "3", "name": "Incidents"},
            "priority": {"id": "5", "name": "Critical"},
        },
    ]


@pytest.fixture
def integration_sample_config_yml(tmp_path: Path) -> Path:
    """Create a temporary valid config.yml file for integration tests."""
    config_content = """
open_ticket_ai:
  api_version: "1"

  infrastructure:
    logging:
      level: "DEBUG"
      log_to_file: false

  services:
    jinja_default:
      use: "base:JinjaRenderer"

    test_ticket_system:
      use: "test:MockedTicketSystem"

  orchestrator:
    use: "base:SimpleSequentialOrchestrator"
    params:
      orchestrator_sleep: "PT0.01S"
    steps:
      - id: test_runner
        use: "base:SimpleSequentialRunner"
        params:
          on:
            id: every_100ms
            use: "base:IntervalTrigger"
            params:
              interval: "PT0.1S"
          run:
            id: test_pipeline
            use: "base:CompositePipe"
            steps:
              - id: fetch_step
                use: "base:FetchTicketsPipe"
                injects:
                  ticket_system: "test_ticket_system"
                params:
                  ticket_search_criteria:
                    queue:
                      name: "Support"
                    limit: 10
"""

    config_file = tmp_path / "config.yml"
    config_file.write_text(config_content)
    return config_file


# ============================================================================
# ENVIRONMENT FIXTURES
# ============================================================================


@pytest.fixture
def integration_env_vars(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Set up environment variables for integration tests."""
    env_vars = {
        "OTAI_TEST_VAR": "test_value",
        "OTAI_API_KEY": "test_api_key_12345",
        "OTAI_TIMEOUT": "30",
        "OTAI_DEBUG": "true",
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    return env_vars


# ============================================================================
# CLEANUP FIXTURES
# ============================================================================


@pytest.fixture(autouse=True)
def integration_test_cleanup():
    """Automatic cleanup after each integration test."""
    # Setup
    yield
    # Teardown - add any cleanup needed after integration tests


# ============================================================================
# HELPER FIXTURES
# ============================================================================


@pytest.fixture
def integration_wait_for_async():
    """Helper to wait for async operations in integration tests."""
    import asyncio

    async def wait(coro, timeout: float = 5.0):
        """Wait for coroutine with timeout."""
        return await asyncio.wait_for(coro, timeout=timeout)

    return wait
