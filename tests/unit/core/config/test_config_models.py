from __future__ import annotations

from pathlib import Path

import pytest

from open_ticket_ai.core import RawOpenTicketAIConfig, load_config


def test_load_config_parses_expected_structure(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        """
        open_ticket_ai:
          plugins:
            - plugin_a
          general_config:
            service:
              url: https://example.com
          services:
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

    config = load_config(config_path)

    assert isinstance(config, RawOpenTicketAIConfig)
    assert config.plugins == ["plugin_a"]
    assert dict(config.general_config)["service"] == {"url": "https://example.com"}
    assert config.services[0].id == "def-1"
    assert dict(config.services[0])["value"] == 42


def test_load_config_missing_root_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="open_ticket_ai"):
        load_config(config_path)
