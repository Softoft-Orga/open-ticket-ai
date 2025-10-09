from __future__ import annotations

from open_ticket_ai.core.template_rendering import (
    JinjaRendererConfig,
    TemplateRendererConfig,
    TemplateRendererEnvConfig,
)


def test_template_renderer_env_config_defaults():
    config = TemplateRendererEnvConfig()
    assert config.prefix == "OTAI_"
    assert config.allowlist is None
    assert config.denylist is None


def test_template_renderer_env_config_custom_values():
    config = TemplateRendererEnvConfig(
        prefix="CUSTOM_",
        allowlist={"CUSTOM_VAR1", "CUSTOM_VAR2"},
        denylist={"CUSTOM_SECRET"},
    )
    assert config.prefix == "CUSTOM_"
    assert config.allowlist == {"CUSTOM_VAR1", "CUSTOM_VAR2"}
    assert config.denylist == {"CUSTOM_SECRET"}


def test_template_renderer_config_defaults():
    config = TemplateRendererConfig(type="jinja")
    assert isinstance(config.env_config, TemplateRendererEnvConfig)
    assert config.env_config.prefix == "OTAI_"


def test_template_renderer_config_custom_env():
    env_config = TemplateRendererEnvConfig(prefix="CUSTOM_")
    config = TemplateRendererConfig(type="jinja", env_config=env_config)
    assert config.env_config.prefix == "CUSTOM_"


def test_jinja_renderer_config_defaults():
    config = JinjaRendererConfig()
    assert config.autoescape is False
    assert config.trim_blocks is True
    assert config.lstrip_blocks is True
    assert isinstance(config.env_config, TemplateRendererEnvConfig)


def test_jinja_renderer_config_custom_values():
    config = JinjaRendererConfig(
        autoescape=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    assert config.autoescape is True
    assert config.trim_blocks is False
    assert config.lstrip_blocks is False


def test_jinja_renderer_config_inherits_env_config():
    env_config = TemplateRendererEnvConfig(prefix="TEST_")
    config = JinjaRendererConfig(env_config=env_config)
    assert config.env_config.prefix == "TEST_"
