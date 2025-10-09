from __future__ import annotations

import os

from open_ticket_ai.core.template_rendering import JinjaRenderer, TemplateRendererEnvConfig, JinjaRendererConfig


def test_jinja_renderer_backward_compatibility_default_params():
    config = JinjaRendererConfig()
    renderer = JinjaRenderer(config=config)
    assert renderer.config.env_config.prefix == "OTAI_"
    assert renderer.config.autoescape is False
    assert renderer.config.trim_blocks is True


def test_jinja_renderer_with_config_object():
    env_config = TemplateRendererEnvConfig(
        prefix="TEST_",
    )

    config = JinjaRendererConfig(
        env_config=env_config,
        autoescape=True,
    )
    renderer = JinjaRenderer(config=config)

    assert renderer.config.env_config.prefix == "TEST_"
    assert renderer.config.autoescape is True


def test_jinja_renderer_filters_env_vars_by_prefix():
    os.environ["TEST_VAR"] = "test_value"
    os.environ["OTHER_VAR"] = "other_value"
    env_config = TemplateRendererEnvConfig(
        prefix="TEST_",
    )

    config = JinjaRendererConfig(
        env_config=env_config,
        autoescape=True,
    )
    renderer = JinjaRenderer(config)
    result = renderer.render("{{ env.TEST_VAR }}", {})

    assert result == "test_value"

    del os.environ["TEST_VAR"]
    del os.environ["OTHER_VAR"]


def test_jinja_renderer_respects_allowlist():
    os.environ["OTAI_ALLOWED"] = "allowed_value"
    os.environ["OTAI_BLOCKED"] = "blocked_value"

    env_config = TemplateRendererEnvConfig(
        prefix="OTAI_",
        allowlist={"OTAI_ALLOWED"},
    )
    config = JinjaRendererConfig(env_config=env_config)
    renderer = JinjaRenderer(config=config)

    result_allowed = renderer.render("{{ env.OTAI_ALLOWED }}", {})
    assert result_allowed == "allowed_value"

    result_blocked = renderer.render("{{ env.get('OTAI_BLOCKED', 'not_found') }}", {})
    assert result_blocked == "not_found"

    del os.environ["OTAI_ALLOWED"]
    del os.environ["OTAI_BLOCKED"]


def test_jinja_renderer_respects_denylist():
    os.environ["OTAI_ALLOWED"] = "allowed_value"
    os.environ["OTAI_DENIED"] = "denied_value"

    env_config = TemplateRendererEnvConfig(
        prefix="OTAI_",
        denylist={"OTAI_DENIED"},
    )
    config = JinjaRendererConfig(env_config=env_config)
    renderer = JinjaRenderer(config=config)

    result_allowed = renderer.render("{{ env.OTAI_ALLOWED }}", {})
    assert result_allowed == "allowed_value"

    result_denied = renderer.render("{{ env.get('OTAI_DENIED', 'not_found') }}", {})
    assert result_denied == "not_found"

    del os.environ["OTAI_ALLOWED"]
    del os.environ["OTAI_DENIED"]


def test_jinja_renderer_renders_template_with_scope():
    config = JinjaRendererConfig()
    renderer = JinjaRenderer(config=config)
    result = renderer.render("Hello {{ name }}!", {"name": "World"})

    assert result == "Hello World!"
