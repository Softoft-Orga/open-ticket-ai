import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from unittest.mock import patch

from rich.console import Console

from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from open_ticket_ai.src.core.config.config_models import ProvidableConfig


class DummyProvidable(Providable):
    pass


def create_config():
    return ProvidableConfig(id="test", params={"a": 1}, provider_key="dummy")


def test_init_pretty_print_called_and_logs(caplog):
    cfg = create_config()
    console = Console()
    with patch(
        "open_ticket_ai.src.core.mixins.registry_providable_instance.pretty_print_config"
    ) as mock_pp, caplog.at_level(logging.INFO):
        DummyProvidable(config=cfg, console=console)
    mock_pp.assert_called_once_with(cfg, console)
    assert "Initializing DummyProvidable with config:" in caplog.text


def test_init_creates_console_when_none_provided():
    cfg = create_config()
    with patch(
        "open_ticket_ai.src.core.mixins.registry_providable_instance.Console"
    ) as mock_console, patch(
        "open_ticket_ai.src.core.mixins.registry_providable_instance.pretty_print_config"
    ):
        obj = DummyProvidable(config=cfg, console=None)
    mock_console.assert_called_once_with()
    assert obj.console is mock_console.return_value


def test_get_provider_key_returns_class_name():
    assert DummyProvidable.get_provider_key() == "DummyProvidable"
