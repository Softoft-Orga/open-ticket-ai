"""Integration tests for JinjaRenderer with real dependencies."""

import pytest

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_simple_string(integration_template_renderer: TemplateRenderer):
    """Test rendering a simple string template with variable substitution."""
    # Given
    template = "Hello {{ name }}!"
    context = {"name": "World"}

    # When
    result = await integration_template_renderer.render(template, context)

    # Then
    assert result == "Hello World!"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_with_pipe_context(
    integration_template_renderer: TemplateRenderer,
    integration_rendering_context: PipeContext,
):
    """Test rendering templates with PipeContext scope including pipe results."""
    # Given
    template = "{{ pipe_results.classify_queue.data.label }}"
    scope = integration_rendering_context.model_dump()

    # When
    result = await integration_template_renderer.render(template, scope)

    # Then
    assert result == "billing"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_with_get_pipe_result_function(
    integration_template_renderer: TemplateRenderer,
):
    """Test rendering with get_pipe_result() custom function."""
    # Given
    template = "{{ get_pipe_result('fetch_tickets', 'fetched_tickets') }}"
    pipe_context = PipeContext(
        pipe_results={
            "fetch_tickets": {
                "succeeded": True,
                "data": {
                    "fetched_tickets": [
                        {"id": "T-1", "subject": "Test"},
                    ],
                },
            }
        }
    )

    # When
    result = await integration_template_renderer.render(template, pipe_context.model_dump())

    # Then
    assert result == [{"id": "T-1", "subject": "Test"}]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_with_has_failed_function(
    integration_template_renderer: TemplateRenderer,
):
    """Test rendering with has_failed() custom function for error checking."""
    # Given
    template = "{% if has_failed('validate') %}Failed{% else %}Success{% endif %}"

    # Context with failed pipe
    pipe_context = PipeContext(
        pipe_results={
            "validate": {
                "succeeded": False,
                "was_skipped": False,
                "message": "Validation error",
                "data": {},
            }
        }
    )

    # When
    result = await integration_template_renderer.render(template, pipe_context.model_dump())

    # Then
    assert result == "Failed"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_list_of_templates(integration_template_renderer: TemplateRenderer):
    """Test rendering a list of template strings."""
    # Given
    templates = [
        "{{ value1 }}",
        "{{ value2 }}",
        "{{ value1 }} and {{ value2 }}",
    ]
    context = {"value1": "first", "value2": "second"}

    # When
    results = await integration_template_renderer.render(templates, context)

    # Then
    assert results == ["first", "second", "first and second"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_dict_of_templates(integration_template_renderer: TemplateRenderer):
    """Test rendering a dictionary with template values."""
    # Given
    template_dict = {
        "name": "{{ username }}",
        "age": "{{ user_age }}",
        "message": "Hello {{ username }}, you are {{ user_age }} years old",
    }
    context = {"username": "Alice", "user_age": 30}

    # When
    result = await integration_template_renderer.render(template_dict, context)

    # Then
    assert result == {
        "name": "Alice",
        "age": 30,  # NativeEnvironment converts "30" to int
        "message": "Hello Alice, you are 30 years old",
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_with_parent_context(integration_template_renderer: TemplateRenderer):
    """Test rendering with parent context access in nested pipes."""
    # Given
    template = "{{ get_parent_param('threshold') }}"

    # Context with parent params
    pipe_context = PipeContext(
        params={"local_param": "value"},
        parent_params={"threshold": 0.8, "model": "test-model"},
    )

    # When
    result = await integration_template_renderer.render(template, pipe_context.model_dump())

    # Then
    assert result == 0.8


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_reads_environment_variable(
    integration_template_renderer: TemplateRenderer, monkeypatch: pytest.MonkeyPatch
):
    """Test rendering when accessing environment variables."""
    template = "{{ get_env('MY_TEST_ENV') }}"
    monkeypatch.setenv("MY_TEST_ENV", "test")
    result = await integration_template_renderer.render(template, {})

    assert result == "test"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_render_conditional_with_pipe_results(
    integration_template_renderer: TemplateRenderer,
):
    """Test conditional template rendering based on pipe results."""
    # Given
    template = """
    {% if get_pipe_result('classify', 'confidence') >= 0.8 %}
    High confidence: {{ get_pipe_result('classify', 'label') }}
    {% else %}
    Low confidence, using fallback
    {% endif %}
    """.strip()

    pipe_context = PipeContext(
        pipe_results={
            "classify": {
                "succeeded": True,
                "data": {
                    "label": "urgent",
                    "confidence": 0.95,
                },
            }
        }
    )

    # When
    result = await integration_template_renderer.render(template, pipe_context.model_dump())

    # Then
    assert "High confidence: urgent" in result
    assert "Low confidence" not in result
