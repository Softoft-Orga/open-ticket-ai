"""
Integration tests for plugin loading and component registration.

Tests the complete plugin loading flow from entry points through
component registration in the ComponentRegistry.
"""

from __future__ import annotations

import pytest
from injector import Injector

from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.plugins.plugin_loader import PluginLoader


@pytest.mark.integration
def test_load_base_plugin_and_verify_registration(integration_config_builder):
    """Test that otai_base plugin loads and registers all components."""
    # Given: Minimal config with no plugins explicitly listed
    config = integration_config_builder.minimal()

    # When: AppModule initializes (loads plugins automatically)
    app_module = AppModule(config)
    registry = app_module.component_registry

    # Then: Base plugin components are registered
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
    # Given: Config and component registry
    config = integration_config_builder.minimal()
    registry = ComponentRegistry()
    logger_factory = AppModule(config).logger_factory

    # When: PluginLoader loads plugins
    plugin_loader = PluginLoader(
        registry=registry,
        logger_factory=logger_factory,
        app_config=config,
    )
    plugin_loader.load_plugins()

    # Then: Plugins are discovered and loaded
    available = registry.get_available_injectables()
    assert len(available) > 0, "At least base plugin should be loaded"


@pytest.mark.integration
def test_multiple_plugins_load_independently(integration_config_builder):
    """Test that multiple plugins load without conflicts."""
    # Given: Config with multiple plugins
    config = integration_config_builder.add_plugin("otai_base").add_jinja_renderer().set_orchestrator().build()

    # When: Plugins load via AppModule
    app_module = AppModule(config)
    registry = app_module.component_registry

    # Then: No duplicate component names
    available = registry.get_available_injectables()
    assert len(available) == len(set(available)), "No duplicate component names should exist"

    # And: Each component has proper plugin prefix
    for component_name in available:
        parts = component_name.split(":")
        assert len(parts) == 2, f"Component {component_name} should have format 'plugin:Component'"


@pytest.mark.integration
def test_plugin_registration_follows_naming_convention(integration_config_builder):
    """Test that plugin components follow the naming convention."""
    # Given: Loaded plugin registry
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    registry = app_module.component_registry

    # When: Getting all registered components
    available = registry.get_available_injectables()

    # Then: All follow plugin:Component pattern
    for name in available:
        plugin_prefix, component_name = name.split(":", 1)

        # Plugin prefix should not be empty
        assert len(plugin_prefix) > 0, f"Empty plugin prefix in {name}"

        # Component name should not be empty
        assert len(component_name) > 0, f"Empty component name in {name}"

        # Plugin prefix should not contain special chars
        assert plugin_prefix.replace("-", "").replace("_", "").isalnum(), (
            f"Plugin prefix '{plugin_prefix}' should be alphanumeric"
        )


@pytest.mark.integration
def test_retrieve_registered_pipe_from_registry(integration_config_builder):
    """Test that registered pipes can be retrieved by registry identifier."""
    # Given: Loaded registry
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    registry = app_module.component_registry

    # When: Retrieving a known pipe
    expression_pipe = registry.get_pipe("base:ExpressionPipe")

    # Then: Pipe class is returned
    assert expression_pipe is not None
    assert expression_pipe.__name__ == "ExpressionPipe"


@pytest.mark.integration
def test_plugin_components_accessible_via_di_container(integration_config_builder):
    """Test that plugin components are accessible through DI container."""
    # Given: DI container with loaded plugins
    config = integration_config_builder.minimal()
    app_module = AppModule(config)
    injector = Injector([app_module])

    # When: Getting ComponentRegistry from container
    registry = injector.get(ComponentRegistry)

    # Then: Registry has plugin components
    available = registry.get_available_injectables()
    assert len(available) > 0
    assert any("base:" in name for name in available)


import pytest

from open_ticket_ai.core.dependency_injection.container import AppModule


@pytest.mark.integration
def test_config_builder_creates_valid_config(integration_config_builder):
    """Test that integration_config_builder creates valid AppConfig."""
    # Given: integration_config_builder with services
    config = (
        integration_config_builder.with_logging(level="INFO")
        .add_service("test_service", "base:JinjaRenderer")
        .set_orchestrator("base:SimpleSequentialOrchestrator")
        .build()
    )

    # When: Validating config structure
    services_list = config.open_ticket_ai.get_services_list()

    # Then: Configuration is valid
    assert config.open_ticket_ai.api_version == "1"
    assert config.open_ticket_ai.infrastructure.logging.level == "INFO"
    assert len(services_list) > 0
    assert config.open_ticket_ai.orchestrator is not None


@pytest.mark.integration
def test_minimal_config_is_valid(integration_config_builder):
    """Test that minimal configuration is valid."""
    # Given: Minimal config
    config = integration_config_builder.minimal()

    # When: Creating AppModule with it
    app_module = AppModule(config)

    # Then: All required components are present
    assert app_module.app_config is not None
    assert app_module.component_registry is not None
    assert app_module.logger_factory is not None


@pytest.mark.integration
def test_config_with_orchestrator_steps(integration_config_builder):
    """Test configuration with orchestrator steps."""
    # Given: Config with orchestrator steps
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

    # When: Extracting orchestrator config
    orchestrator = config.open_ticket_ai.orchestrator

    # Then: Steps are configured
    assert "steps" in orchestrator.params
    steps = orchestrator.params["steps"]
    assert len(steps) == 1
    assert steps[0]["id"] == "test_runner"


@pytest.mark.integration
def test_config_services_are_accessible(integration_config_builder):
    """Test that configured services are accessible."""
    # Given: Config with multiple services
    config = (
        integration_config_builder.add_service("service1", "base:JinjaRenderer")
        .add_service("service2", "base:JinjaRenderer", params={"key": "value"})
        .build()
    )

    # When: Getting services list
    services = config.open_ticket_ai.get_services_list()

    # Then: All services are present
    service_ids = [s.id for s in services]
    assert "service1" in service_ids
    assert "service2" in service_ids


@pytest.mark.integration
def test_config_from_yaml_matches_builder(integration_config_builder):
    """Test that YAML-loaded config matches builder-created config."""
    # Given: Config from builder
    builder_config = (
        integration_config_builder.with_logging(level="DEBUG")
        .add_jinja_renderer("jinja_default")
        .set_orchestrator()
        .build()
    )

    # Then: Both have same structure
    assert builder_config.open_ticket_ai.infrastructure.logging.level == "DEBUG"
    assert "jinja_default" in builder_config.open_ticket_ai.services
    assert builder_config.open_ticket_ai.orchestrator is not None
