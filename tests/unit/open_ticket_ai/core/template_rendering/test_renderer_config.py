from __future__ import annotations

import os

from open_ticket_ai.core.template_rendering.renderer_config import (
    TemplateRendererEnvConfig,
    TemplateRendererConfig,
    JinjaRendererConfig,
)


def test_template_renderer_env_config_defaults():
    config = TemplateRendererEnvConfig()
    assert config.prefix == "OTAI_"
    assert config.extra_prefixes == ()
    assert config.allowlist is None
    assert config.denylist is None
    assert config.key == "env"
    assert config.provider is None
    assert config.refresh_on_each_render is False


def test_template_renderer_env_config_custom_values():
    config = TemplateRendererEnvConfig(
        prefix="CUSTOM_",
        extra_prefixes=("EXTRA_", "MORE_"),
        allowlist={"CUSTOM_VAR1", "CUSTOM_VAR2"},
        denylist={"CUSTOM_SECRET"},
        key="custom_env",
        refresh_on_each_render=True,
    )
    assert config.prefix == "CUSTOM_"
    assert config.extra_prefixes == ("EXTRA_", "MORE_")
    assert config.allowlist == {"CUSTOM_VAR1", "CUSTOM_VAR2"}
    assert config.denylist == {"CUSTOM_SECRET"}
    assert config.key == "custom_env"
    assert config.refresh_on_each_render is True


def test_template_renderer_env_config_with_provider():
    def custom_provider():
        return {"TEST_VAR": "test_value"}
    
    config = TemplateRendererEnvConfig(provider=custom_provider)
    assert config.provider is not None
    assert config.provider() == {"TEST_VAR": "test_value"}


def test_template_renderer_config_defaults():
    config = TemplateRendererConfig()
    assert isinstance(config.env_config, TemplateRendererEnvConfig)
    assert config.env_config.prefix == "OTAI_"


def test_template_renderer_config_custom_env():
    env_config = TemplateRendererEnvConfig(prefix="CUSTOM_", key="myenv")
    config = TemplateRendererConfig(env_config=env_config)
    assert config.env_config.prefix == "CUSTOM_"
    assert config.env_config.key == "myenv"


def test_jinja_renderer_config_defaults():
    config = JinjaRendererConfig()
    assert config.env is None
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
    env_config = TemplateRendererEnvConfig(
        prefix="TEST_",
        key="test_env",
        refresh_on_each_render=True,
    )
    config = JinjaRendererConfig(env_config=env_config)
    assert config.env_config.prefix == "TEST_"
    assert config.env_config.key == "test_env"
    assert config.env_config.refresh_on_each_render is True


def test_jinja_renderer_config_model_dump_excludes_callables():
    def custom_provider():
        return {"TEST": "value"}
    
    env_config = TemplateRendererEnvConfig(provider=custom_provider)
    config = JinjaRendererConfig(env_config=env_config)
    
    dumped = config.model_dump()
    assert "provider" not in dumped["env_config"]
    assert "env" not in dumped
