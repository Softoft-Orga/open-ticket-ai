from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT / "src") not in sys.path:
    sys.path.append(str(ROOT / "src"))

# Provide a minimal yaml module stub so config_models can be imported without optional dependency
if "yaml" not in sys.modules:
    yaml_stub = types.ModuleType("yaml")
    yaml_stub.safe_load = lambda stream: {}
    sys.modules["yaml"] = yaml_stub

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import (
    RawOpenTicketAIConfig,
    RenderedOpenTicketAIConfig,
    RenderedSystemConfig,
    SystemConfig,
)


def test_system_config_render_resolves_templates():
    scope = {
        "general_config": {"provider_key": "otobo", "timeout": 30},
        "defs": {
            "base_url": "https://example.com",
            "flags": {"secure": True},
        },
    }

    raw_config = SystemConfig(
        id="service",
        provider_key="{{ general_config.provider_key }}",
        config={
            "api_url": "{{ defs.base_url }}/api",
            "timeout": "{{ general_config.timeout }}",
            "flags": "{{ defs.flags }}",
        },
    )

    rendered_data = raw_config.render(scope)
    rendered_config = RenderedSystemConfig(**rendered_data)

    assert rendered_config.provider_key == "otobo"
    assert rendered_config.config["api_url"] == "https://example.com/api"
    assert rendered_config.config["timeout"] == 30
    assert rendered_config.config["flags"] == {"secure": True}


class _RenderScope(BaseModel):
    general_config: dict
    defs: dict


def test_open_ticket_ai_config_render_with_base_model_scope():
    scope = _RenderScope(
        general_config={
            "provider_key": "znuny",
            "base_url": "https://tickets.example.com",
        },
        defs={
            "api_path": "/api/v1",
            "extra_plugin": "notifications",
            "interval": 45,
            "system_config": {"retries": 5},
        },
    )

    raw_config = RawOpenTicketAIConfig(
        version="2.0.0",
        plugins=["core", "{{ defs.extra_plugin }}"],
        general_config={
            "base_url": "https://tickets.example.com",
            "timeout": "{{ defs.interval }}",
        },
        defs={},
        system=SystemConfig(
            id="primary",
            provider_key="{{ general_config.provider_key }}",
            config={
                "api_url": "{{ general_config.base_url }}{{ defs.api_path }}",
                "retries": "{{ defs.system_config.retries }}",
            },
        ),
    )

    rendered_data = raw_config.render(scope)
    rendered_config = RenderedOpenTicketAIConfig(**rendered_data)

    assert rendered_config.plugins == ["core", "notifications"]
    assert rendered_config.general_config["timeout"] == 45
    assert isinstance(rendered_config.system, RenderedSystemConfig)
    assert rendered_config.system.provider_key == "znuny"
    assert rendered_config.system.config["api_url"] == "https://tickets.example.com/api/v1"
    assert rendered_config.system.config["retries"] == 5
