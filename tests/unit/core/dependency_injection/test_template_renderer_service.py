from __future__ import annotations

from pathlib import Path

import pytest
from injector import Injector

from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


def test_template_renderer_bootstrapped_from_services(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
    default_template_renderer: "jinja_default"
  services:
    - id: "jinja_default"
      use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
      params:
        env_config:
          prefix: "OTAI_"
        autoescape: false
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    renderer = injector.get(TemplateRenderer)  # type: ignore[type-abstract]

    assert isinstance(renderer, JinjaRenderer)
    assert renderer.config.env_config.prefix == "OTAI_"
    assert renderer.config.autoescape is False


def test_template_renderer_with_custom_params(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
    default_template_renderer: "custom_jinja"
  services:
    - id: "custom_jinja"
      use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
      params:
        env_config:
          prefix: "CUSTOM_"
          allowlist: ["CUSTOM_VAR1", "CUSTOM_VAR2"]
        autoescape: true
        trim_blocks: false
        lstrip_blocks: false
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    renderer = injector.get(TemplateRenderer)  # type: ignore[type-abstract]

    assert isinstance(renderer, JinjaRenderer)
    assert renderer.config.env_config.prefix == "CUSTOM_"
    assert renderer.config.env_config.allowlist == {"CUSTOM_VAR1", "CUSTOM_VAR2"}
    assert renderer.config.autoescape is True
    assert renderer.config.trim_blocks is False
    assert renderer.config.lstrip_blocks is False


def test_template_renderer_not_found_raises_error(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
    default_template_renderer: "nonexistent"
  services:
    - id: "jinja_default"
      use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
      params:
        env_config:
          prefix: "OTAI_"
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    with pytest.raises(ValueError, match="Template renderer service with id 'nonexistent' not found"):
        injector.get(TemplateRenderer)  # type: ignore[type-abstract]


def test_template_renderer_invalid_class_raises_error(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
    default_template_renderer: "invalid_renderer"
  services:
    - id: "invalid_renderer"
      use: "open_ticket_ai.core.config.config_loader:ConfigLoader"
      params: {}
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    with pytest.raises(TypeError, match="is not a TemplateRenderer subclass"):
        injector.get(TemplateRenderer)  # type: ignore[type-abstract]


def test_template_renderer_uses_default_when_not_specified(tmp_path: Path) -> None:
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
  services:
    - id: "jinja_default"
      use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
      params:
        env_config:
          prefix: "OTAI_"
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")

    injector = Injector([AppModule(config_path)])
    renderer = injector.get(TemplateRenderer)  # type: ignore[type-abstract]

    assert isinstance(renderer, JinjaRenderer)
