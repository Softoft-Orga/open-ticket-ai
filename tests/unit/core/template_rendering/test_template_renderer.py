import re
from typing import Any

import pytest
from pydantic import BaseModel

from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class SimpleParams(BaseModel):
    pass


class SimpleTemplateRenderer(TemplateRenderer[SimpleParams]):
    ParamsModel = SimpleParams

    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory) -> None:
        super().__init__(config, logger_factory)

    def _render(self, template_str: str, scope: dict[str, Any]) -> str:
        result = template_str
        for key, value in scope.items():
            pattern = r"\{\{" + re.escape(key) + r"\}\}"
            result = re.sub(pattern, str(value), result)
        return result


@pytest.mark.parametrize(
    "obj,scope,expected",
    [
        ("Hello {{name}}", {"name": "World"}, "Hello World"),
        ("{{greeting}} {{name}}", {"greeting": "Hi", "name": "Alice"}, "Hi Alice"),
        ("No template", {}, "No template"),
        ("{{key}}", {"key": "value", "unused": "data"}, "value"),
    ],
    ids=["simple_string", "multiple_placeholders", "no_placeholders", "extra_scope_data"],
)
def test_render_string(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = renderer.render(obj, scope)
    assert result == expected


@pytest.mark.parametrize(
    "obj,scope,expected",
    [
        (["{{a}}", "{{b}}"], {"a": "first", "b": "second"}, ["first", "second"]),
        (["plain", "{{key}}"], {"key": "value"}, ["plain", "value"]),
        ([], {}, []),
        (["{{x}}", "static", "{{y}}"], {"x": "1", "y": "2"}, ["1", "static", "2"]),
    ],
    ids=["list_all_templates", "list_mixed", "empty_list", "list_multiple"],
)
def test_render_list(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = renderer.render(obj, scope)
    assert result == expected


@pytest.mark.parametrize(
    "obj,scope,expected",
    [
        ({"key": "{{value}}"}, {"value": "result"}, {"key": "result"}),
        ({"a": "{{x}}", "b": "{{y}}"}, {"x": "1", "y": "2"}, {"a": "1", "b": "2"}),
        ({}, {}, {}),
        ({"static": "value", "dynamic": "{{key}}"}, {"key": "data"}, {"static": "value", "dynamic": "data"}),
    ],
    ids=["dict_single", "dict_multiple", "empty_dict", "dict_mixed"],
)
def test_render_dict(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = renderer.render(obj, scope)
    assert result == expected


@pytest.mark.parametrize(
    "obj,scope,expected",
    [
        ({"outer": {"inner": "{{key}}"}}, {"key": "value"}, {"outer": {"inner": "value"}}),
        (
            {"a": {"b": {"c": "{{deep}}"}}},
            {"deep": "nested"},
            {"a": {"b": {"c": "nested"}}},
        ),
        (
            {"list": ["{{x}}", "{{y}}"], "dict": {"z": "{{z}}"}},
            {"x": "1", "y": "2", "z": "3"},
            {"list": ["1", "2"], "dict": {"z": "3"}},
        ),
    ],
    ids=["nested_dict", "deeply_nested", "mixed_structures"],
)
def test_render_nested_dict(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = renderer.render(obj, scope)
    assert result == expected
