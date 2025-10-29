import re
from typing import Any

import pytest
from pydantic import BaseModel, Field

from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.template_rendering.template_renderer import (
    NoRenderField,
    TemplateRenderer,
    TemplateRenderError,
)


class SimpleParams(BaseModel):
    pass


class SimpleTemplateRenderer(TemplateRenderer[SimpleParams]):
    ParamsModel = SimpleParams

    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory) -> None:
        super().__init__(config, logger_factory)

    async def _render(self, template_str: str, scope: dict[str, Any]) -> str:
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
@pytest.mark.asyncio
async def test_render_string(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = await renderer.render(obj, scope)
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
@pytest.mark.asyncio
async def test_render_list(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = await renderer.render(obj, scope)
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
@pytest.mark.asyncio
async def test_render_dict(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = await renderer.render(obj, scope)
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
@pytest.mark.asyncio
async def test_render_nested_dict(logger_factory, obj, scope, expected):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)
    result = await renderer.render(obj, scope)
    assert result == expected


class ModelWithNoRenderField(BaseModel):
    renderable_field: str = Field(default="{{value}}")
    non_renderable_field: str = NoRenderField(default="{{value}}")


class ModelAllRenderableFields(BaseModel):
    field_a: str = Field(default="{{a}}")
    field_b: str = Field(default="{{b}}")


class ModelAllNonRenderableFields(BaseModel):
    field_x: str = NoRenderField(default="{{x}}")
    field_y: str = NoRenderField(default="{{y}}")


class ModelMixedFields(BaseModel):
    template_field: str = Field(default="{{template}}")
    config_field: list[dict[str, Any]] = NoRenderField(default_factory=list)
    static_field: str = Field(default="static")


class ModelNestedNoRenderField(BaseModel):
    outer: str = Field(default="{{outer}}")
    nested: dict[str, Any] = NoRenderField(default_factory=dict)


@pytest.mark.asyncio
async def test_render_to_model_with_no_render_field(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"renderable_field": "{{value}}", "non_renderable_field": "{{value}}"}
    scope = {"value": "rendered"}

    result = await renderer.render_to_model(ModelWithNoRenderField, raw_dict, scope)

    assert result.renderable_field == "rendered"
    assert result.non_renderable_field == "{{value}}"


@pytest.mark.asyncio
async def test_render_to_model_all_renderable(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"field_a": "{{a}}", "field_b": "{{b}}"}
    scope = {"a": "first", "b": "second"}

    result = await renderer.render_to_model(ModelAllRenderableFields, raw_dict, scope)

    assert result.field_a == "first"
    assert result.field_b == "second"


@pytest.mark.asyncio
async def test_render_to_model_all_non_renderable(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"field_x": "{{x}}", "field_y": "{{y}}"}
    scope = {"x": "rendered_x", "y": "rendered_y"}

    result = await renderer.render_to_model(ModelAllNonRenderableFields, raw_dict, scope)

    assert result.field_x == "{{x}}"
    assert result.field_y == "{{y}}"


@pytest.mark.asyncio
async def test_render_to_model_mixed_fields(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"template_field": "{{template}}", "config_field": [{"key": "{{value}}"}], "static_field": "static"}
    scope = {"template": "rendered", "value": "should_not_render"}

    result = await renderer.render_to_model(ModelMixedFields, raw_dict, scope)

    assert result.template_field == "rendered"
    assert result.config_field == [{"key": "{{value}}"}]
    assert result.static_field == "static"


@pytest.mark.asyncio
async def test_render_to_model_nested_no_render_field(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"outer": "{{outer}}", "nested": {"inner": "{{inner}}"}}
    scope = {"outer": "outer_rendered", "inner": "inner_value"}

    result = await renderer.render_to_model(ModelNestedNoRenderField, raw_dict, scope)

    assert result.outer == "outer_rendered"
    assert result.nested == {"inner": "{{inner}}"}


@pytest.mark.asyncio
async def test_render_to_model_partial_fields(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"renderable_field": "{{value}}"}
    scope = {"value": "rendered"}

    result = await renderer.render_to_model(ModelWithNoRenderField, raw_dict, scope)

    assert result.renderable_field == "rendered"
    assert result.non_renderable_field == "{{value}}"


@pytest.mark.asyncio
async def test_render_to_model_empty_scope(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    raw_dict = {"renderable_field": "no_template", "non_renderable_field": "{{value}}"}
    scope = {}

    result = await renderer.render_to_model(ModelWithNoRenderField, raw_dict, scope)

    assert result.renderable_field == "no_template"
    assert result.non_renderable_field == "{{value}}"


@pytest.mark.asyncio
async def test_render_to_model_validation_error(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    class StrictModel(BaseModel):
        required_field: int

    raw_dict = {"required_field": "{{value}}"}
    scope = {"value": "not_an_int"}

    with pytest.raises(TemplateRenderError):
        await renderer.render_to_model(StrictModel, raw_dict, scope)


@pytest.mark.asyncio
async def test_no_render_field_preserves_complex_structures(logger_factory):
    config = InjectableConfig(id="test-renderer")
    renderer = SimpleTemplateRenderer(config, logger_factory)

    complex_config = [
        {"use": "pipe1", "params": {"key": "{{value}}"}},
        {"use": "pipe2", "params": {"key": "{{another}}"}},
    ]

    raw_dict = {
        "template_field": "{{template}}",
        "config_field": complex_config,
    }
    scope = {"template": "rendered", "value": "x", "another": "y"}

    result = await renderer.render_to_model(ModelMixedFields, raw_dict, scope)

    assert result.template_field == "rendered"
    assert result.config_field == complex_config
