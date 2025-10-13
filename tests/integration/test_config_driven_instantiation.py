"""Integration tests for config-driven instantiation and DI.

Tests verify that YAML config can be loaded, services are registered correctly,
and the entire system (pipes, services, triggers) is instantiated from config
with proper dependency injection.
"""

from __future__ import annotations

from pathlib import Path

from injector import Injector

from open_ticket_ai.core import AppConfig, AppModule, ConfigLoader, RawOpenTicketAIConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator import Orchestrator
from open_ticket_ai.core.orchestration.orchestrator_config import OrchestratorConfig


def test_config_loading_and_service_registration(tmp_path: Path, logger_factory: LoggerFactory) -> None:
    """Test that config loading registers services correctly."""
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services:
    - id: mock_ticket_system
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    config_loader = ConfigLoader(AppConfig(), logger_factory)
    config = config_loader.load_config(config_path)

    assert config.services is not None
    assert len(config.services) == 1
    assert config.services[0].id == "mock_ticket_system"
    assert config.services[0].use == "tests.unit.mocked_ticket_system:MockedTicketSystem"


def test_di_container_instantiation_from_config(tmp_path: Path) -> None:
    """Test that DI container can be created from config and provides required services."""
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services:
    - id: test_service
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    config = injector.get(RawOpenTicketAIConfig)
    assert config.services is not None
    assert len(config.services) == 1

    logger_factory = injector.get(LoggerFactory)
    assert logger_factory is not None

    renderable_factory = injector.get(RenderableFactory)
    assert renderable_factory is not None


def test_orchestrator_instantiation_from_config(tmp_path: Path) -> None:
    """Test that Orchestrator can be instantiated from config with triggers."""
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services: []
  orchestrator:
    runners:
      - id: test_runner
        "on":
          - id: interval_trigger_1
            use: open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger
            params:
              seconds: 5
        run:
          id: test_pipe
          use: open_ticket_ai.base.pipes.composite_pipe:CompositePipe
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    orchestrator_config = injector.get(OrchestratorConfig)
    assert orchestrator_config is not None
    assert len(orchestrator_config.runners) == 1
    assert orchestrator_config.runners[0].id == "test_runner"
    assert orchestrator_config.runners[0].run.id == "test_pipe"

    orchestrator = injector.get(Orchestrator)
    assert orchestrator is not None


def test_end_to_end_config_to_runtime_instantiation(tmp_path: Path) -> None:
    """Test complete end-to-end flow from config loading to runtime object creation."""
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services:
    - id: mock_ticket_system
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
  orchestrator:
    runners:
      - id: fetch_runner
        "on":
          - id: interval_trigger
            use: open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger
            params:
              seconds: 10
        run:
          id: fetch_tickets
          use: open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe:FetchTicketsPipe
          params:
            ticket_search_criteria:
              limit: 10
          injects:
            ticket_system_service: mock_ticket_system
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    config = injector.get(RawOpenTicketAIConfig)
    assert config is not None
    assert len(config.services) == 1
    assert config.services[0].id == "mock_ticket_system"

    logger_factory = injector.get(LoggerFactory)
    assert logger_factory is not None

    renderable_factory = injector.get(RenderableFactory)
    assert renderable_factory is not None

    orchestrator_config = injector.get(OrchestratorConfig)
    assert orchestrator_config is not None
    assert len(orchestrator_config.runners) == 1
    assert orchestrator_config.runners[0].run.id == "fetch_tickets"

    orchestrator = injector.get(Orchestrator)
    assert orchestrator is not None


def test_config_with_multiple_services_and_pipes(tmp_path: Path) -> None:
    """Test config with multiple services and pipe definitions."""
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services:
    - id: mock_ticket_system_1
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
    - id: mock_ticket_system_2
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
  orchestrator:
    runners:
      - id: runner_1
        "on":
          - id: trigger_1
            use: open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger
            params:
              seconds: 5
        run:
          id: pipe_1
          use: open_ticket_ai.base.pipes.composite_pipe:CompositePipe
      - id: runner_2
        "on":
          - id: trigger_2
            use: open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger
            params:
              seconds: 10
        run:
          id: pipe_2
          use: open_ticket_ai.base.pipes.composite_pipe:CompositePipe
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])

    config = injector.get(RawOpenTicketAIConfig)
    assert len(config.services) == 2
    assert config.services[0].id == "mock_ticket_system_1"
    assert config.services[1].id == "mock_ticket_system_2"

    orchestrator_config = injector.get(OrchestratorConfig)
    assert len(orchestrator_config.runners) == 2
    assert orchestrator_config.runners[0].id == "runner_1"
    assert orchestrator_config.runners[1].id == "runner_2"


def test_config_with_custom_app_config(tmp_path: Path) -> None:
    """Test config loading with custom AppConfig settings."""
    config_content = """
my_custom_app:
  plugins: ["custom-plugin"]
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "custom_config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    custom_app_config = AppConfig(config_yaml_root_key="my_custom_app")
    injector = Injector([AppModule(config_path, custom_app_config)])

    config = injector.get(RawOpenTicketAIConfig)
    assert config.plugins == ["custom-plugin"]

    app_config = injector.get(AppConfig)
    assert app_config.config_yaml_root_key == "my_custom_app"


def test_pipe_instantiation_via_renderable_factory(tmp_path: Path) -> None:
    """Test that config with services is properly loaded and can be used for DI.

    This test verifies that services defined in config are registered and available
    for dependency injection into pipes.
    """
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
      disable_existing_loggers: false
      formatters:
        simple:
          format: '%(levelname)s - %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          formatter: simple
      root:
        level: INFO
        handlers: [console]
  services:
    - id: mock_ticket_system
      use: tests.unit.mocked_ticket_system:MockedTicketSystem
      params: {}
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    renderable_factory = injector.get(RenderableFactory)

    assert renderable_factory is not None
    assert len(renderable_factory._registerable_configs) == 1
    assert renderable_factory._registerable_configs[0].id == "mock_ticket_system"
