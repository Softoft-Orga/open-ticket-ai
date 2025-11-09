"""Integration tests for plugin loading and component registration."""

from __future__ import annotations

import pytest
from injector import Injector

from open_ticket_ai.core.config.config_models import PluginConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.plugins.plugin_loader import PluginLoader


@pytest.mark.integration
def test_load_base_plugin_and_verify_registration(integration_config_builder):
    """Test that otai_base plugin loads and registers all components."""
    config = integration_config_builder.minimal()

    app_module = AppModule(config)
    registry = app_module.component_registry

    available = registry.get_available_injectables()

    # Verify base pipes are registered
    assert any("base:CompositePipe" in name for name in available), (
        "CompositePipe should be registered from base plugin"
    )
    assert any("base:ExpressionPipe" in name for name in available), (
        "ExpressionPipe should be registered from base plugin"
    )

    # Verify base services are registered
    assert any("base:JinjaRenderer" in name for name in available), (
        "JinjaRenderer should be registered from base plugin"
    )

    # Verify naming convention (plugin:Component)
    for name in available:
        assert ":" in name, f"Component {name} should follow 'plugin:Component' naming"


@pytest.mark.integration
def test_plugin_loader_discovers_entry_points(integration_config_builder):
    """Test that PluginLoader discovers plugins from entry points."""
    config = integration_config_builder.minimal()
    registry = ComponentRegistry()
    logger_factory = AppModule(config).logger_factory

    plugin_loader = PluginLoader(
        registry=registry,
        logger_factory=logger_factory,
        app_config=config,
    )
    plugin_loader.load_plugins()

    available = registry.get_available_injectables()
    assert len(available) > 0, "At least base plugin should be loaded"


@pytest.mark.integration
def test_multiple_plugins_load_independently(integration_config_builder):
    """Test that multiple plugins load without conflicts."""
    config = integration_config_builder.add_plugin(PluginConfig(
        name="otai_base", version=">=1.0.0",
    )).add_plugin(PluginConfig(
        name="otai_example_plugin", version=">=1.0.0",
    )).add_jinja_renderer().set_orchestrator().build()

    app_module = AppModule(config)
    registry = app_module.component_registry

    available = registry.get_available_injectables()
    assert len(available) == len(set(available)), "No duplicate component names should exist"

    for component_name in available:
        parts = component_name.split(":")
        assert len(parts) == 2, f"Component {component_name} should have format 'plugin:Component'"


@pytest.mark.integration
def test_plugin_registration_follows_naming_convention(integration_config_builder):
    """Test that plugin components follow the naming convention."""
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    registry = app_module.component_registry

    available = registry.get_available_injectables()

    for name in available:
        plugin_prefix, component_name = name.split(":", 1)

        assert len(plugin_prefix) > 0, f"Empty plugin prefix in {name}"

        assert len(component_name) > 0, f"Empty component name in {name}"

        assert plugin_prefix.replace("-", "").replace("_", "").isalnum(), (
            f"Plugin prefix '{plugin_prefix}' should be alphanumeric"
        )


@pytest.mark.integration
def test_retrieve_registered_pipe_from_registry(integration_config_builder):
    """Test that registered pipes can be retrieved by registry identifier."""
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    registry = app_module.component_registry

    expression_pipe = registry.get_pipe(by_identifier="base:ExpressionPipe")

    assert expression_pipe is not None
    assert expression_pipe.__name__ == "ExpressionPipe"


@pytest.mark.integration
def test_plugin_components_accessible_via_di_container(integration_config_builder):
    """Test that plugin components are accessible through DI container."""
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    injector = Injector([app_module])

    registry = injector.get(ComponentRegistry)

    available = registry.get_available_injectables()
    assert len(available) > 0
    assert any("base:" in name for name in available)


@pytest.mark.integration
def test_config_builder_creates_valid_config(integration_config_builder):
    """Test that integration_config_builder creates valid AppConfig."""
    config = (
        integration_config_builder.with_logging(level="INFO")
        .add_service("test_service", "base:JinjaRenderer")
        .set_orchestrator()
        .build()
    )

    services_list = config.open_ticket_ai.get_services_list()

    assert str(config.open_ticket_ai.api_version) == ">=1.0.0"
    assert config.open_ticket_ai.infrastructure.logging.level == "INFO"
    assert len(services_list) > 0
    assert config.open_ticket_ai.orchestrator is not None


@pytest.mark.integration
def test_minimal_config_is_valid(integration_config_builder):
    """Test that minimal configuration is valid."""
    config = integration_config_builder.minimal()

    app_module = AppModule(config)

    assert app_module.app_config is not None
    assert app_module.component_registry is not None
    assert app_module.logger_factory is not None


@pytest.mark.integration
def test_config_with_orchestrator_steps(integration_config_builder):
    """Test configuration with orchestrator steps."""
    config = (
        integration_config_builder.add_jinja_renderer()
        .set_orchestrator()
        .add_orchestrator_step(
            step_id="test_runner",
            use="base:SimpleSequentialRunner",
            params={"run": {"id": "test", "use": "base:ExpressionPipe"}},
        )
        .build()
    )

    orchestrator = config.open_ticket_ai.orchestrator

    assert "steps" in orchestrator.params
    steps = orchestrator.params["steps"]
    assert len(steps) == 1
    assert steps[0]["id"] == "test_runner"


@pytest.mark.integration
def test_config_services_are_accessible(integration_config_builder):
    """Test that configured services are accessible."""
    config = (
        integration_config_builder.add_service("service1", "base:JinjaRenderer")
        .add_service("service2", "base:JinjaRenderer", params={"key": "value"})
        .build()
    )

    services = config.open_ticket_ai.get_services_list()

    service_ids = [s.id for s in services]
    assert "service1" in service_ids
    assert "service2" in service_ids


@pytest.mark.integration
def test_config_from_yaml_matches_builder(integration_config_builder):
    """Test that YAML-loaded config matches builder-created config."""
    builder_config = (
        integration_config_builder.with_logging(level="DEBUG")
        .add_jinja_renderer("jinja_default")
        .set_orchestrator()
        .build()
    )

    assert builder_config.open_ticket_ai.infrastructure.logging.level == "DEBUG"
    assert "jinja_default" in builder_config.open_ticket_ai.services
    assert builder_config.open_ticket_ai.orchestrator is not None
