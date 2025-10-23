from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from packages.otai_hf_local.src.otai_hf_local.hf_local_plugin import create_hf_local_plugin


def test_plugin_registration_with_valid_config():
    app_config = AppConfig()
    mock_registry = MagicMock(spec=ComponentRegistry)

    plugin_instance = create_hf_local_plugin(app_config)
    plugin_instance.on_load(mock_registry)

    assert mock_registry.register.called
    assert mock_registry.register.call_count >= 1


def test_plugin_callable_with_invalid_config_raises_error():
    with pytest.raises(AttributeError):
        plugin_instance = create_hf_local_plugin(None)
        plugin_instance.on_load(MagicMock())
