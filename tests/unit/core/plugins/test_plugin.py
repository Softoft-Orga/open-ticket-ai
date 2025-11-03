from unittest.mock import MagicMock, PropertyMock

import pytest

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.errors import RegistryError
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.plugins.plugin import Plugin
from tests.unit.conftest import SimpleInjectable


class TestConcretePlugin(Plugin):
    def __init__(self, app_config: AppConfig, injectables: list[type[SimpleInjectable]] | None = None):
        super().__init__(app_config)
        self._injectables = injectables if injectables is not None else []

    def _get_all_injectables(self) -> list[type[SimpleInjectable]]:
        return self._injectables


@pytest.fixture
def app_config_for_plugin():
    mock = MagicMock(spec=AppConfig)
    type(mock).PLUGIN_NAME_PREFIX = PropertyMock(return_value="otai-")
    type(mock).REGISTRY_IDENTIFIER_SEPERATOR = PropertyMock(return_value=":")
    return mock


class TestOnLoad:
    def test_on_load_registers_all_injectables(self, app_config_for_plugin, mock_component_registry):
        injectables = [SimpleInjectable]
        plugin = TestConcretePlugin(app_config_for_plugin, injectables)

        plugin.on_load(mock_component_registry)

        mock_component_registry.register.assert_called_once()
        registry_name, injectable_class = mock_component_registry.register.call_args[0]
        assert injectable_class == SimpleInjectable
        assert "SimpleInjectable" in registry_name

    def test_on_load_with_multiple_injectables(self, app_config_for_plugin, mock_component_registry):
        injectables = [SimpleInjectable, SimpleInjectable]
        plugin = TestConcretePlugin(app_config_for_plugin, injectables)

        plugin.on_load(mock_component_registry)

        assert mock_component_registry.register.call_count == 2

    def test_on_load_with_empty_injectables_does_not_call_register(
        self, app_config_for_plugin, mock_component_registry
    ):
        plugin = TestConcretePlugin(app_config_for_plugin, [])

        plugin.on_load(mock_component_registry)

        mock_component_registry.register.assert_not_called()

    def test_on_load_propagates_registry_error(self, app_config_for_plugin):
        mock_registry = MagicMock(spec=ComponentRegistry)
        mock_registry.get_available_injectables.return_value = [SimpleInjectable]
        mock_registry.register.side_effect = RegistryError(mock_registry, "Test error")
        plugin = TestConcretePlugin(app_config_for_plugin, [SimpleInjectable])

        with pytest.raises(RegistryError, match="Test error"):
            plugin.on_load(mock_registry)
