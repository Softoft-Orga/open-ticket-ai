from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry

from otai_hf_local.plugin import plugin


def test_plugin_registration_with_valid_config():
    app_config = AppConfig()
    mock_registry = MagicMock(spec=ComponentRegistry)
    
    plugin_instance = plugin(app_config)
    plugin_instance.on_load(mock_registry)
    
    assert mock_registry.register.called
    assert mock_registry.register.call_count >= 1
    
    expected_prefix = f"hf-local{app_config.REGISTRY_IDENTIFIER_SEPERATOR}"
    call_args_list = mock_registry.register.call_args_list
    hf_local_registrations = [
        call
        for call in call_args_list
        if call.args
        and len(call.args) > 0
        and isinstance(call.args[0], str)
        and call.args[0].startswith(expected_prefix)
    ]
    assert len(hf_local_registrations) >= 1


def test_plugin_callable_with_invalid_config_raises_error():
    with pytest.raises(AttributeError):
        plugin_instance = plugin(None)
        plugin_instance.on_load(MagicMock())
