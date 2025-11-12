import json

import pytest

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import LoggingConfig, PipeConfig

__TESTING_CLASS__ = AppConfig

from open_ticket_ai.core.config.types import VersionSpecifier


@pytest.mark.integration
def test_appconfig_reads_yaml_open_ticket_ai_key(tmp_path, monkeypatch):
    yml = """
open_ticket_ai:
  api_version: ">=9.0.0"
  plugins:
    - name: "otai-base"
      version: ">=1.0.0"
    - name: "otai-extra"
      version: ">=2.0.0"
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
    assert str(cfg.open_ticket_ai.api_version) == ">=9.0.0"
    assert cfg.open_ticket_ai.plugins[0].name == "otai-base"
    assert cfg.open_ticket_ai.plugins[0].version == ">=1.0.0"
    assert cfg.open_ticket_ai.plugins[1].name == "otai-extra"
    assert cfg.open_ticket_ai.plugins[1].version == ">=2.0.0"
    assert isinstance(cfg.open_ticket_ai.infrastructure.logging, LoggingConfig)
    assert cfg.open_ticket_ai.infrastructure.logging.level == "WARNING"
    assert isinstance(cfg.open_ticket_ai.orchestrator, PipeConfig)
    assert cfg.open_ticket_ai.orchestrator.id == "orch"
    assert cfg.open_ticket_ai.orchestrator.use == "core:CompositePipe"


@pytest.mark.integration
def test_appconfig_reads_yaml_with_cfg_alias(tmp_path, monkeypatch):
    yml = """
cfg:
  api_version: ">=2.0.0"
  plugins:
    - name: "otai-alias"
      version: ">=1.0.0"
"""
    (tmp_path / "config.yml").write_text(yml)
    monkeypatch.chdir(tmp_path)
    cfg = AppConfig()
    assert str(cfg.open_ticket_ai.api_version) == ">=2.0.0"
    assert cfg.open_ticket_ai.plugins[0].name == "otai-alias"


@pytest.mark.integration
def test_appconfig_env_overrides_and_combines_with_yaml(tmp_path, monkeypatch):
    yml = """
open_ticket_ai:
  plugins:
    - name: "otai-yaml-a"
      version: ">=1.0.0"
    - name: "otai-yaml-b"
      version: ">=2.0.0"
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
    monkeypatch.setenv("OPEN_TICKET_AI__API_VERSION", ">=3.0.0")
    monkeypatch.setenv("OPEN_TICKET_AI__API_VERSION", ">=3.0.0")
    cfg = AppConfig()
    assert cfg.open_ticket_ai.plugins[1].name == "otai-yaml-b"
    assert str(cfg.open_ticket_ai.api_version) == ">=3.0.0"
    assert cfg.open_ticket_ai.infrastructure.logging.level == "ERROR"
    assert cfg.open_ticket_ai.orchestrator.id == "orch-yaml"
    assert cfg.open_ticket_ai.orchestrator.use == "core:CompositePipe"

