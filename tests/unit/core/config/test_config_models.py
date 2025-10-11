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
          infrastructure:
            service:
              url: https://example.com
          defs:
            - id: def-1
              value: 42
          orchestrator:
            runners:
                - run_every_milli_seconds: 5000
                  pipe:
                    id: orchestrator-step
                    type: some.pipe
                

        """.strip(),
        encoding="utf-8",
    )

    config_loader = ConfigLoader(AppConfig())
    config = config_loader.load_config(config_path)

    assert isinstance(config, RawOpenTicketAIConfig)
    assert config.plugins == ["plugin_a"]
    assert dict(config.infrastructure)["service"] == {"url": "https://example.com"}
    assert config.defs[0].id == "def-1"
    assert dict(config.defs[0])["value"] == 42


def test_load_config_missing_root_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text("{}", encoding="utf-8")

    config_loader = ConfigLoader(AppConfig())
    with pytest.raises(KeyError):
        config_loader.load_config(config_path)
