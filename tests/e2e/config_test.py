from pathlib import Path

import pytest

pytest.importorskip("pydantic")
from open_ticket_ai.src.core.config.config_models import load_config


def test_load_yaml_config():
    config = load_config(Path(__file__).parent / 'config.yml')
    print(config)
