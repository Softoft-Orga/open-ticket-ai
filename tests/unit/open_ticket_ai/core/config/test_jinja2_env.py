import pytest
from pydantic import BaseModel

from open_ticket_ai.core.config import jinja2_env


class ExampleModel(BaseModel):
    name: str
    score: int


@pytest.mark.parametrize(
    "template, scope, expected",
    [
        ("Hello {{ name }}", {"name": "Alice"}, "Hello Alice"),
        ("{{ value }}", {"value": 123}, 123),
        ("{\"foo\": {{ value }}}", {"value": 42}, {"foo": 42}),
        ("{{ items }}", {"items": "[1, 2, 3]"}, [1, 2, 3]),
        ("{{ score }}", ExampleModel(name="Eve", score=7), 7),
    ],
)
def test_render_parses_output_and_supports_basemodel_scope(template, scope, expected):
    assert jinja2_env.render(template, scope) == expected


def test_render_fail_silently_returns_original_template():
    with pytest.raises(ZeroDivisionError):
        jinja2_env.render("{{ 1 / 0 }}", {})

    assert jinja2_env.render("{{ 1 / 0 }}", {}, fail_silently=True) == "{{ 1 / 0 }}"


def test_render_recursive_handles_nested_structures():
    template = {
        "greeting": "Hello {{ name }}",
        "numbers": ["{{ first }}", "{{ second }}"],
        "nested": {"json": "{\"count\": {{ count }}}"},
    }
    scope = {"name": "Bob", "first": 1, "second": 2, "count": 3}

    assert jinja2_env.render_recursive(template, scope) == {
        "greeting": "Hello Bob",
        "numbers": [1, 2],
        "nested": {"json": {"count": 3}},
    }


def test_render_recursive_fail_silently_propagates():
    template = ["{{ 1 / 0 }}", "{{ value }}"]

    assert jinja2_env.render_recursive(template, {"value": "ok"}, fail_silently=True) == [
        "{{ 1 / 0 }}",
        "ok",
    ]
