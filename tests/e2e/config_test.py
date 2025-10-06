from pathlib import Path

from open_ticket_ai.open_ticket_ai.core.config import load_config


def test_load_yaml_config():
    config = load_config(Path(__file__).parent / "config.yml")
    print(config)
