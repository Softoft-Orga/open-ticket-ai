from open_ticket_ai.core.config.jinja2_env import LazyTemplate, render_any, render_text
from open_ticket_ai.core.pipeline.context import PipelineContext


def test_render_text_returns_lazy_template():
    """Test that render_text returns a LazyTemplate instance for string inputs."""
    scope = {"var": "value"}
    result = render_text("{{ var }}", scope)
    assert isinstance(result, LazyTemplate)
    assert str(result) == "value"


def test_render_text_non_string_returns_unchanged():
    """Test that non-string values are returned unchanged."""
    value = {"key": "value"}
    result = render_text(value, {})
    assert result is value


def test_lazy_template_renders_on_access():
    """Test that the template is only rendered when accessed."""
    scope = {"name": "test"}
    template = LazyTemplate("Hello {{ name }}", scope)

    # Template shouldn't be rendered yet
    assert not template._is_rendered

    # Accessing the value should trigger rendering
    assert str(template) == "Hello test"
    assert template._is_rendered
    assert template._rendered_value == "Hello test"


def test_lazy_template_caches_result():
    """Test that the template result is cached after first render."""
    scope = {"counter": 0}

    def increment_counter():
        scope["counter"] += 1
        return str(scope["counter"])

    scope["increment"] = increment_counter
    template = LazyTemplate("{{ increment() }}", scope)

    # First access should call increment
    assert str(template) == "1"

    # Second access should use cached value
    assert str(template) == "1"
    assert scope["counter"] == 1  # increment was only called once


def test_lazy_template_dict_access():
    """Test dictionary-style access on rendered templates."""
    scope = {"data": {"key": "value"}}
    template = LazyTemplate("{{ data }}", scope)

    # Should be able to access dict items
    assert template["key"] == "value"
    assert template.get("key") == "value"
    assert template.get("nonexistent", "default") == "default"


def test_render_any_with_dict():
    """Test that render_any processes dictionary values recursively."""
    scope = {"var": "value"}
    input_dict = {"key1": "{{ var }}", "nested": {"key2": "nested {{ var }}"}, "list": ["{{ var }}", "static"]}

    result = render_any(input_dict, PipelineContext(data=scope))

    # Top level
    assert isinstance(result["key1"], LazyTemplate)
    assert str(result["key1"]) == "value"

    # Nested dict
    assert isinstance(result["nested"]["key2"], LazyTemplate)
    assert str(result["nested"]["key2"]) == "nested value"

    # List items
    assert isinstance(result["list"][0], LazyTemplate)
    assert str(result["list"][0]) == "value"
    assert result["list"][1] == "static"  # Non-template strings unchanged


def test_render_any_with_list():
    """Test that render_any processes list items."""
    scope = {"items": [1, 2, 3]}
    input_list = ["{{ items[0] }}", "{{ items[1] }}", "static"]

    result = render_any(input_list, PipelineContext(data=scope))

    assert len(result) == 3
    assert str(result[0]) == "1"
    assert str(result[1]) == "2"
    assert result[2] == "static"  # Non-template strings unchanged


def test_lazy_template_error_handling(caplog):
    """Test that template errors are caught and logged."""
    template = LazyTemplate("{{ undefined_var }}", {})

    # Access should not raise but log a warning
    result = str(template)

    assert "'undefined_var' is undefined" in caplog.text
    assert result == "{{ undefined_var }}"  # Returns original string on error
