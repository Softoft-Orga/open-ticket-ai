from __future__ import annotations

from pathlib import Path

import pytest

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig, load_config


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
          defs:
            - id: def-1
              value: 42
          orchestrator:
            - id: orchestrator-step
              type: some.pipe
        """.strip(),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert isinstance(config, RawOpenTicketAIConfig)
    assert config.plugins == ["plugin_a"]
    assert config.general_config == {"service": {"url": "https://example.com"}}
    assert config.defs == [{"id": "def-1", "value": 42}]
    assert config.orchestrator == [{"id": "orchestrator-step", "type": "some.pipe"}]


def test_load_config_missing_root_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="open_ticket_ai"):
        load_config(config_path)


def test_raw_open_ticket_ai_config_defaults_are_isolated() -> None:
    first = RawOpenTicketAIConfig()
    second = RawOpenTicketAIConfig()

    first.plugins.append("plugin-a")
    first.general_config["a"] = {"b": 1}
    first.defs.append({"id": "def"})
    first.orchestrator.append({"id": "orchestrator"})

    assert second.plugins == []
    assert second.general_config == {}
    assert second.defs == []
    assert second.orchestrator == []
