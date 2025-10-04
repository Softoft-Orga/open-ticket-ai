"""Tests for the flow editor API service module."""

import tempfile
from pathlib import Path

import pytest

from open_ticket_ai.api.service import (
    convert_yaml_to_mermaid,
    load_config_yaml,
    save_config_yaml,
)


def test_load_config_yaml():
    """Test loading YAML configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"
        yaml_content = "key: value"
        config_path.write_text(yaml_content, encoding="utf-8")

        loaded = load_config_yaml(config_path)
        assert loaded == yaml_content


def test_load_config_yaml_not_found():
    """Test loading non-existent configuration raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_config_yaml(Path("/nonexistent/config.yml"))


def test_save_config_yaml():
    """Test saving YAML configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"
        yaml_content = "key: new_value"

        save_config_yaml(config_path, yaml_content)

        assert config_path.exists()
        assert config_path.read_text(encoding="utf-8") == yaml_content


def test_convert_yaml_to_mermaid_with_existing_config():
    """Test converting existing config file to Mermaid."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"
        yaml_content = """
open_ticket_ai:
  defs:
    - id: test_pipeline
      steps:
        - id: step1
        - id: step2
          depends_on: [step1]
"""
        config_path.write_text(yaml_content, encoding="utf-8")

        result = convert_yaml_to_mermaid(None, config_path)

        assert "flowchart TD" in result or "flowchart LR" in result
        assert "test_pipeline" in result


def test_convert_yaml_to_mermaid_with_inline_yaml():
    """Test converting inline YAML to Mermaid."""
    yaml_content = """
open_ticket_ai:
  defs:
    - id: inline_pipeline
      steps:
        - id: step1
        - id: step2
          depends_on: [step1]
"""
    result = convert_yaml_to_mermaid(yaml_content, Path("dummy.yml"), direction="TD")

    assert "flowchart TD" in result
    assert "inline_pipeline" in result


def test_convert_yaml_to_mermaid_with_lr_direction():
    """Test converting YAML to Mermaid with LR direction."""
    yaml_content = """
open_ticket_ai:
  defs:
    - id: lr_pipeline
      steps:
        - id: step1
        - id: step2
          depends_on: [step1]
"""
    result = convert_yaml_to_mermaid(yaml_content, Path("dummy.yml"), direction="LR")

    assert "flowchart LR" in result
    assert "lr_pipeline" in result


def test_convert_yaml_to_mermaid_empty_config():
    """Test converting empty config returns default message."""
    yaml_content = """
open_ticket_ai:
  defs: []
"""
    result = convert_yaml_to_mermaid(yaml_content, Path("dummy.yml"))

    assert "No pipelines found" in result
