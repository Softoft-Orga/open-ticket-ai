import json

import pytest

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import LoggingConfig, PipeConfig


@pytest.mark.integration
def test_appconfig_reads_yaml_open_ticket_ai_key(tmp_path, monkeypatch):
    yml = """
open_ticket_ai:
  api_version: "9"
  plugins: ["otai-base","otai-extra"]
  infrastructure:
    logging:
      level: "WARNING"
  orchestrator:
    id: "orch"
    use: "core:CompositePipe"
"""
    (tmp_path / "config.yml").write_text(yml)
    monkeypatch.chdir(tmp_path)
    cfg = AppConfig()
    assert cfg.open_ticket_ai.api_version == "9"
    assert cfg.open_ticket_ai.plugins == ["otai-base", "otai-extra"]
    assert isinstance(cfg.open_ticket_ai.infrastructure.logging, LoggingConfig)
    assert cfg.open_ticket_ai.infrastructure.logging.level == "WARNING"
    assert isinstance(cfg.open_ticket_ai.orchestrator, PipeConfig)
    assert cfg.open_ticket_ai.orchestrator.id == "orch"
    assert cfg.open_ticket_ai.orchestrator.use == "core:CompositePipe"


@pytest.mark.integration
def test_appconfig_reads_yaml_with_cfg_alias(tmp_path, monkeypatch):
    yml = """
cfg:
  api_version: "2"
  plugins: ["otai-alias"]
"""
    (tmp_path / "config.yml").write_text(yml)
    monkeypatch.chdir(tmp_path)
    cfg = AppConfig()
    assert cfg.open_ticket_ai.api_version == "2"
    assert cfg.open_ticket_ai.plugins == ["otai-alias"]


@pytest.mark.integration
def test_appconfig_env_overrides_and_combines_with_yaml(tmp_path, monkeypatch):
    yml = """
open_ticket_ai:
  plugins: ["otai-yaml-a","otai-yaml-b"]
  infrastructure:
    logging:
      level: "INFO"
  orchestrator:
    id: "orch-yaml"
    use: "core:CompositePipe"
"""
    (tmp_path / "config.yml").write_text(yml)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPEN_TICKET_AI__INFRASTRUCTURE__LOGGING__LEVEL", "ERROR")
    monkeypatch.setenv("OPEN_TICKET_AI__API_VERSION", "3")
    monkeypatch.setenv("OPEN_TICKET_AI__API_VERSION", "3")
    cfg = AppConfig()
    assert cfg.open_ticket_ai.plugins == ["otai-yaml-a", "otai-yaml-b"]
    assert cfg.open_ticket_ai.api_version == "3"
    assert cfg.open_ticket_ai.infrastructure.logging.level == "ERROR"
    assert cfg.open_ticket_ai.orchestrator.id == "orch-yaml"
    assert cfg.open_ticket_ai.orchestrator.use == "core:CompositePipe"


@pytest.mark.integration
def test_appconfig_env_can_override_lists_when_needed(tmp_path, monkeypatch):
    yml = """
open_ticket_ai:
  plugins: ["otai-yaml-a","otai-yaml-b"]
"""
    (tmp_path / "config.yml").write_text(yml)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPEN_TICKET_AI__PLUGINS", json.dumps(["otai-env-a", "otai-env-b"]))
    cfg = AppConfig()
    assert cfg.open_ticket_ai.plugins == ["otai-env-a", "otai-env-b"]
