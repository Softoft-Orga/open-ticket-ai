from unittest.mock import MagicMock

import pytest
from open_ticket_ai import AppConfig
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry

from otai_hf_local.hf_local_plugin import HFLocalPlugin


def test_plugin_registration_with_valid_config():
    app_config = AppConfig()
    mock_registry = MagicMock(spec=ComponentRegistry)

    plugin_instance = HFLocalPlugin(app_config)
    plugin_instance.on_load(mock_registry)

    assert mock_registry.register.called
    assert mock_registry.register.call_count >= 1

