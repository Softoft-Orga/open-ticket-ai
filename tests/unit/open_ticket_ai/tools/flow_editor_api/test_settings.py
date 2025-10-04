"""Tests for the flow editor API settings."""

import os
from pathlib import Path

from open_ticket_ai.tools.flow_editor_api.settings import Settings, get_settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    assert settings.config_path == Path("src/config.yml")
    assert settings.cors_origins == ["http://localhost:5173"]


def test_settings_with_env_var(monkeypatch):
    """Test settings with CONFIG_PATH environment variable."""
    custom_path = "/custom/config.yml"
    monkeypatch.setenv("CONFIG_PATH", custom_path)
    
    settings = Settings()
    assert settings.config_path == Path(custom_path)


def test_get_settings():
    """Test get_settings function."""
    settings = get_settings()
    assert isinstance(settings, Settings)
