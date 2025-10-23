from __future__ import annotations

import pytest

from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from packages.base.src.otai_base.template_renderers.jinja_renderer import JinjaRenderer


@pytest.fixture
def jinja_renderer(logger_factory: LoggerFactory) -> JinjaRenderer:
    config = InjectableConfig(id="test-jinja-renderer")
    return JinjaRenderer(config=config, logger_factory=logger_factory)


def test_render_simple_variable(jinja_renderer: JinjaRenderer) -> None:
    template = "Hello {{ name }}!"
    context = {"name": "World"}
    result = jinja_renderer.render(template, context)
    assert result == "Hello World!"


def test_render_multiple_variables(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ greeting }} {{ name }}!"
    context = {"greeting": "Hello", "name": "World"}
    result = jinja_renderer.render(template, context)
    assert result == "Hello World!"


def test_render_simple_calculation(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ 5 + 5 }}"
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result == 10


def test_render_string_filter_lower(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ 'TEXT' | lower }}"
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result == "text"


def test_render_string_filter_upper(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ 'text' | upper }}"
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result == "TEXT"


def test_render_list(jinja_renderer: JinjaRenderer) -> None:
    template_list = ["Item {{ index }}: {{ name }}", "Count: {{ count }}"]
    context = {"index": 1, "name": "Apple", "count": 5}
    result = jinja_renderer.render(template_list, context)
    assert result == ["Item 1: Apple", "Count: 5"]


def test_render_dict(jinja_renderer: JinjaRenderer) -> None:
    template_dict = {"greeting": "Hello {{ name }}", "count": "{{ 5 * 2 }}"}
    context = {"name": "World"}
    result = jinja_renderer.render(template_dict, context)
    assert result == {"greeting": "Hello World", "count": 10}


def test_render_nested_dict(jinja_renderer: JinjaRenderer) -> None:
    template_dict = {"outer": {"inner": "Value: {{ value }}"}}
    context = {"value": "test"}
    result = jinja_renderer.render(template_dict, context)
    assert result == {"outer": {"inner": "Value: test"}}


def test_custom_function_at_path_in_globals(jinja_renderer: JinjaRenderer) -> None:
    result = jinja_renderer.render("{{ at_path is defined }}", {})
    assert result is True


def test_custom_function_has_failed_in_globals(jinja_renderer: JinjaRenderer) -> None:
    result = jinja_renderer.render("{{ has_failed is defined }}", {})
    assert result is True


def test_custom_function_get_pipe_result_in_globals(jinja_renderer: JinjaRenderer) -> None:
    result = jinja_renderer.render("{{ get_pipe_result is defined }}", {})
    assert result is True


def test_render_missing_variable_returns_empty_string(jinja_renderer: JinjaRenderer) -> None:
    template = "Hello {{ undefined_var }}!"
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result == "Hello !"


def test_render_with_conditional(jinja_renderer: JinjaRenderer) -> None:
    template = "{% if show_message %}Message: {{ message }}{% endif %}"
    context = {"show_message": True, "message": "Hello"}
    result = jinja_renderer.render(template, context)
    assert result == "Message: Hello"


def test_render_with_loop(jinja_renderer: JinjaRenderer) -> None:
    template = "{% for item in items %}{{ item }} {% endfor %}"
    context = {"items": ["a", "b", "c"]}
    result = jinja_renderer.render(template, context)
    assert result == "a b c "


def test_render_boolean_value(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ value }}"
    context = {"value": True}
    result = jinja_renderer.render(template, context)
    assert result is True


def test_render_numeric_values(jinja_renderer: JinjaRenderer) -> None:
    template = "{{ int_val }} {{ float_val }}"
    context = {"int_val": 42, "float_val": 3.14}
    result = jinja_renderer.render(template, context)
    assert result == "42 3.14"


def test_render_empty_string(jinja_renderer: JinjaRenderer) -> None:
    template = ""
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result is None


def test_render_with_trim_blocks(jinja_renderer: JinjaRenderer) -> None:
    template = "{% if True %}\nvalue\n{% endif %}"
    context: dict[str, str] = {}
    result = jinja_renderer.render(template, context)
    assert result.strip() == "value"
