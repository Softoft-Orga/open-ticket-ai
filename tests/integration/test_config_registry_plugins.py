import pytest

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.plugins.plugin_loader import PluginLoader


@pytest.mark.integration
def test_config_loading_from_file(temp_config_file):
    app_config = AppConfig(_env_file=None)
    
    assert app_config.open_ticket_ai is not None
    assert app_config.open_ticket_ai.api_version == "1"
    assert "jinja_default" in app_config.open_ticket_ai.services


@pytest.mark.integration
def test_registry_contains_expected_components(integration_container):
    from open_ticket_ai.base.plugin import BasePlugin
    
    registry = integration_container.get(ComponentRegistry)
    app_config = integration_container.get(AppConfig)
    
    base_plugin = BasePlugin(app_config)
    base_plugin.on_load(registry)
    
    available_injectables = registry.get_available_injectables()
    
    assert len(available_injectables) > 0, "Registry should contain components"
    
    assert any("JinjaRenderer" in name for name in available_injectables), \
        "Registry should contain JinjaRenderer"
    assert any("FetchTicketsPipe" in name for name in available_injectables), \
        "Registry should contain FetchTicketsPipe"


@pytest.mark.integration
def test_plugin_discovery_and_loading(integration_container):
    from open_ticket_ai.base.plugin import BasePlugin
    
    registry = integration_container.get(ComponentRegistry)
    app_config = integration_container.get(AppConfig)
    
    base_plugin = BasePlugin(app_config)
    base_plugin.on_load(registry)
    
    available_injectables = registry.get_available_injectables()
    
    assert len(available_injectables) > 0, "Registry should contain plugins after loading"
    
    base_components = [name for name in available_injectables if name.startswith("base:")]
    assert len(base_components) > 0, "Registry should contain base plugin components"


@pytest.mark.integration
def test_registry_identifier_format(integration_container):
    from open_ticket_ai.base.plugin import BasePlugin
    
    registry = integration_container.get(ComponentRegistry)
    app_config = integration_container.get(AppConfig)
    
    base_plugin = BasePlugin(app_config)
    base_plugin.on_load(registry)
    
    available_injectables = registry.get_available_injectables()
    
    base_components = [name for name in available_injectables if ":" in name]
    assert len(base_components) > 0, "Registry should use 'plugin:Component' format"
    
    expected_format_components = [
        name for name in available_injectables 
        if ":" in name and not name.startswith("open_ticket_ai.")
    ]
    assert len(expected_format_components) > 0, \
        "Registry identifiers should use 'base:ComponentName' format, not full class paths"


@pytest.mark.integration
def test_at_least_one_pipe_service_and_plugin_registered(integration_container):
    from open_ticket_ai.base.plugin import BasePlugin
    
    registry = integration_container.get(ComponentRegistry)
    app_config = integration_container.get(AppConfig)
    
    base_plugin = BasePlugin(app_config)
    base_plugin.on_load(registry)
    
    available_injectables = registry.get_available_injectables()
    
    pipes = [name for name in available_injectables if "Pipe" in name or "Orchestrator" in name or "Runner" in name]
    services = [name for name in available_injectables if "Renderer" in name or "Service" in name]
    plugins = [name for name in available_injectables if ":" in name]
    
    assert len(pipes) > 0, "At least one pipe should be registered"
    assert len(services) > 0, "At least one service should be registered"
    assert len(plugins) > 0, "At least one plugin should be registered"


@pytest.mark.integration
def test_base_plugin_loaded_with_correct_identifiers(integration_container):
    from open_ticket_ai.base.plugin import BasePlugin
    
    registry = integration_container.get(ComponentRegistry)
    app_config = integration_container.get(AppConfig)
    
    base_plugin = BasePlugin(app_config)
    base_plugin.on_load(registry)
    
    available_injectables = registry.get_available_injectables()
    
    assert "base:JinjaRenderer" in available_injectables, \
        "Registry should contain 'base:JinjaRenderer'"
    assert "base:FetchTicketsPipe" in available_injectables, \
        "Registry should contain 'base:FetchTicketsPipe'"
    assert "base:SimpleSequentialOrchestrator" in available_injectables, \
        "Registry should contain 'base:SimpleSequentialOrchestrator'"
