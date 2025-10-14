"""
Tests to validate the Pipe params pattern documented in AGENTS.md and developer docs.
This ensures documentation examples work correctly.

Note: In production, RenderableFactory.create_pipe() calls render_params() which converts
EmptyParams -> dict -> rendered dict, then passes that to Pipe.__init__. This test simulates
that by directly passing dicts to test the Pipe validation logic.
"""

from typing import Any

import pydantic
import pytest

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import ParamsModel, Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


class ExamplePipeParams(ParamsModel):
    """Example params model as shown in documentation."""

    threshold: float
    model: str
    max_items: int = 100


class ExamplePipeResultData(pydantic.BaseModel):
    """Example result data model."""

    processed_count: int


class ExamplePipe(Pipe):
    """Example pipe following the documented pattern."""

    params_class = ExamplePipeParams

    def __init__(
        self,
        pipe_config: PipeConfig,
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory)

    async def _process(self) -> PipeResult:
        return PipeResult(
            success=True,
            failed=False,
            data=ExamplePipeResultData(processed_count=self.params["max_items"]),
        )


@pytest.mark.asyncio
async def test_pipe_params_dict_validation(logger_factory: LoggerFactory) -> None:
    """Test that params as dict get validated to Pydantic model.

    This simulates what RenderableFactory does: it converts EmptyParams to dict,
    renders templates, then passes the dict to Pipe which validates it.
    """
    params_dict = {"threshold": 0.8, "model": "gpt-4", "max_items": 50}

    # Create config with dict params (simulating post-rendering state)
    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_dict  # Bypass Pydantic validation, assign dict directly

    # Pipe.__init__ should validate dict -> ExamplePipeParams
    pipe = ExamplePipe(pipe_config=config, logger_factory=logger_factory)

    # Verify final params are the correct type
    assert isinstance(pipe.params, ExamplePipeParams)
    assert pipe.params.threshold == 0.8
    assert pipe.params.model == "gpt-4"
    assert pipe.params.max_items == 50


@pytest.mark.asyncio
async def test_pipe_params_dict_with_type_coercion(logger_factory: LoggerFactory) -> None:
    """Test that type coercion works (simulating template rendering).

    Templates render to strings, which need to be coerced to proper types.
    """
    params_dict = {
        "threshold": "0.7",
        "model": "claude",
        "max_items": "25",
    }

    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_dict

    pipe = ExamplePipe(pipe_config=config, logger_factory=logger_factory)

    # Pydantic should have coerced string values to proper types
    assert isinstance(pipe.params, ExamplePipeParams)
    assert pipe.params.threshold == 0.7
    assert pipe.params.model == "claude"
    assert pipe.params.max_items == 25


@pytest.mark.asyncio
async def test_pipe_params_dict_with_defaults(logger_factory: LoggerFactory) -> None:
    """Test that defaults work when not provided in dict."""
    params_dict = {"threshold": 0.9, "model": "llama"}

    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_dict

    pipe = ExamplePipe(pipe_config=config, logger_factory=logger_factory)

    # max_items should use default value
    assert pipe.params.max_items == 100


@pytest.mark.asyncio
async def test_pipe_params_typed_model(logger_factory: LoggerFactory) -> None:
    """Test that params can also be provided as typed Pydantic model."""
    params_model = ExamplePipeParams(threshold=0.85, model="gemini", max_items=200)

    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_model

    pipe = ExamplePipe(pipe_config=config, logger_factory=logger_factory)

    # When params is already a model, it should be used as-is (if not dict)
    # Actually, any non-dict BaseModel will be used as params directly
    assert pipe.params.threshold == 0.85
    assert pipe.params.model == "gemini"
    assert pipe.params.max_items == 200


@pytest.mark.asyncio
async def test_pipe_execution_with_dict_params(logger_factory: LoggerFactory) -> None:
    """Test full pipe execution with dict params."""
    params_dict = {"threshold": 0.6, "model": "mistral", "max_items": 75}

    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_dict

    pipe = ExamplePipe(pipe_config=config, logger_factory=logger_factory)

    context = PipeContext()
    result_context = await pipe.process(context)

    assert "test_pipe" in result_context.pipe_results
    pipe_result = result_context.pipe_results["test_pipe"]
    assert pipe_result.success is True
    assert pipe_result.data.processed_count == 75


@pytest.mark.asyncio
async def test_pipe_params_validation_error(logger_factory: LoggerFactory) -> None:
    """Test that invalid params raise validation error during Pipe init."""
    params_dict = {
        "threshold": "not_a_number",
        "model": "valid-model",
    }

    config: PipeConfig[Any] = PipeConfig(id="test_pipe")
    config.params = params_dict

    # Error should occur in Pipe.__init__ when validating dict -> ExamplePipeParams
    with pytest.raises(pydantic.ValidationError):
        ExamplePipe(pipe_config=config, logger_factory=logger_factory)
