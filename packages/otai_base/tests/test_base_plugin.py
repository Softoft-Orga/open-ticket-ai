from unittest.mock import MagicMock

from open_ticket_ai import Plugin
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry

from otai_base.base_plugin import BasePlugin

MIN_REGISTERED_COMPONENTS = 2


class TestBasePlugin:
    def test_plugin_function_returns_plugin_instance(self, mock_app_config):
        result = BasePlugin(mock_app_config)

        assert isinstance(result, Plugin)
        assert isinstance(result, BasePlugin)

    def test_on_load_registers_all_injectables(self, mock_app_config):
        mock_app_config.PLUGIN_NAME_PREFIX = "otai-"
        mock_app_config.REGISTRY_IDENTIFIER_SEPERATOR = ":"
        mock_registry = MagicMock(spec=ComponentRegistry)
        base_plugin = BasePlugin(mock_app_config)

        base_plugin.on_load(mock_registry)

        assert mock_registry.register.call_count >= MIN_REGISTERED_COMPONENTS

    def test_registry_identifier_format(self, mock_app_config):
        mock_app_config.PLUGIN_NAME_PREFIX = "otai-"
        mock_app_config.REGISTRY_IDENTIFIER_SEPERATOR = ":"
        mock_registry = MagicMock(spec=ComponentRegistry)
        base_plugin = BasePlugin(mock_app_config)

        base_plugin.on_load(mock_registry)

        registered_names = [call[0][0] for call in mock_registry.register.call_args_list]
        assert any(name.startswith("base:") for name in registered_names)
