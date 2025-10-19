from unittest.mock import MagicMock

from open_ticket_ai.base.plugin import BasePlugin, plugin
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.plugins.plugin_base import Plugin


class TestBasePlugin:
    def test_plugin_function_returns_plugin_instance(self, mock_app_config):
        result = plugin(mock_app_config)

        assert isinstance(result, Plugin)
        assert isinstance(result, BasePlugin)

    def test_on_load_registers_all_injectables(self, mock_app_config):
        mock_app_config.PLUGIN_NAME_PREFIX = "otai-"
        mock_app_config.REGISTRY_IDENTIFIER_SEPERATOR = ":"
        mock_registry = MagicMock(spec=ComponentRegistry)
        base_plugin = BasePlugin(mock_app_config)

        base_plugin.on_load(mock_registry)

        assert mock_registry.register.call_count >= 2

    def test_registry_identifier_format(self, mock_app_config):
        mock_app_config.PLUGIN_NAME_PREFIX = "otai-"
        mock_app_config.REGISTRY_IDENTIFIER_SEPERATOR = ":"
        mock_registry = MagicMock(spec=ComponentRegistry)
        base_plugin = BasePlugin(mock_app_config)

        base_plugin.on_load(mock_registry)

        registered_names = [call[0][0] for call in mock_registry.register.call_args_list]
        assert any(name.startswith("base:") for name in registered_names)
