"""
End-to-end test demonstrating the new Renderable pattern.
"""

import pytest
from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


class CustomPipeParams(BaseModel):
    """Example typed params model."""

    message: str
    multiplier: int = 1


class CustomPipeConfig(Renderable[CustomPipeParams]):
    """Example pipe config using Renderable pattern."""

    pass


class CustomPipe(Pipe):
    """Example pipe using typed params."""

    def __init__(self, pipe_params: CustomPipeConfig, *args, **kwargs):
        super().__init__(pipe_params)
        if isinstance(pipe_params, dict):
            self.config = CustomPipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, CustomPipeConfig):
            self.config = pipe_params
        else:
            self.config = CustomPipeConfig.model_validate(pipe_params.model_dump())

    async def _process(self) -> PipeResult:
        # Access typed params with full IDE support
        message = self.config.params.message * self.config.params.multiplier
        return PipeResult(success=True, failed=False, data={"result": message})


@pytest.mark.asyncio
async def test_renderable_pattern_end_to_end():
    """Test the complete Renderable pattern with a custom pipe."""
    # Create config using dict (automatic conversion to typed model)
    config = {
        "id": "custom_pipe",
        "use": "CustomPipe",
        "params": {"message": "Hello", "multiplier": 3},
    }

    # Create pipe
    pipe = CustomPipe(config)

    # Verify params are typed
    assert isinstance(pipe.config.params, CustomPipeParams)
    assert pipe.config.params.message == "Hello"
    assert pipe.config.params.multiplier == 3

    # Process pipe
    context = PipeContext(pipes={}, params={})
    result_context = await pipe.process(context)

    # Verify result
    result = result_context.pipes["custom_pipe"]
    assert result.success is True
    assert result.data["result"] == "HelloHelloHello"


@pytest.mark.asyncio
async def test_renderable_pattern_with_typed_object():
    """Test creating config with typed params object."""
    # Create params object
    params = CustomPipeParams(message="World", multiplier=2)

    # Create config with typed params
    config = CustomPipeConfig(id="custom_pipe", params=params)

    # Verify params are typed
    assert isinstance(config.params, CustomPipeParams)
    assert config.params.message == "World"
    assert config.params.multiplier == 2

    # Create and process pipe
    pipe = CustomPipe(config)
    context = PipeContext(pipes={}, params={})
    result_context = await pipe.process(context)

    # Verify result
    result = result_context.pipes["custom_pipe"]
    assert result.success is True
    assert result.data["result"] == "WorldWorld"


def test_renderable_backward_compatibility():
    """Test backward compatibility with dict params."""
    from open_ticket_ai.core.config.registerable import RegisterableConfig

    # Old pattern still works
    config = RegisterableConfig(id="old_style", params={"any": "value"})
    assert config.id == "old_style"
    assert isinstance(config.params, dict)
    assert config.params == {"any": "value"}
