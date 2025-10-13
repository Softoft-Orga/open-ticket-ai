from __future__ import annotations

from pathlib import Path

import pytest

from open_ticket_ai.core import AppConfig, ConfigLoader
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


def test_load_config_parses_expected_structure(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        """
        open_ticket_ai:
          plugins:
            - plugin_a
          services:
            - id: def-1
              params:
                value: 42
          orchestrator:
            runners:
                - "on":
                    - use: open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger
                      params:
                        milliseconds: 5000
                  run:
                    id: orchestrator-step
                    use: some.pipe
                

        """.strip(),
        encoding="utf-8",
    )

    config_loader = ConfigLoader(AppConfig())
    config = config_loader.load_config(config_path)

    assert isinstance(config, RawOpenTicketAIConfig)
    assert config.plugins == ["plugin_a"]
    assert config.services[0].id == "def-1"
    assert config.services[0].params["value"] == 42


def test_load_config_missing_root_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text("{}", encoding="utf-8")

    config_loader = ConfigLoader(AppConfig())
    with pytest.raises(ValueError):
        config_loader.load_config(config_path)
