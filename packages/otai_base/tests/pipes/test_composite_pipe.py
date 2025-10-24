from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult

from otai_base.pipes.composite_pipe import CompositePipe

ALPHABET_START = ord("A")


@pytest.fixture
def mock_pipe_factory():
    factory = MagicMock(spec=PipeFactory)
    factory.create_pipe = AsyncMock()
    return factory


@pytest.fixture
def simple_step_configs() -> list[PipeConfig]:
    return [
        PipeConfig(id="step1", use="tests.unit.conftest.SimplePipe", params={"value": "A"}),
        PipeConfig(id="step2", use="tests.unit.conftest.SimplePipe", params={"value": "B"}),
        PipeConfig(id="step3", use="tests.unit.conftest.SimplePipe", params={"value": "C"}),
    ]


async def test_composite_pipe_with_empty_steps(mock_pipe_factory, logger_factory, empty_pipeline_context):
    config = PipeConfig(id="composite", use="CompositePipe", params={})
    composite = CompositePipe(pipe_factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    result = await composite.process(empty_pipeline_context)

    assert result.succeeded
    assert result.data == {}
    mock_pipe_factory.create_pipe.assert_not_called()


async def test_composite_pipe_with_none_steps(mock_pipe_factory, logger_factory, empty_pipeline_context):
    config = PipeConfig(id="composite", use="CompositePipe", params={})
    composite = CompositePipe(pipe_factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    result = await composite.process(empty_pipeline_context)

    assert result.succeeded
    assert result.data == {}
    mock_pipe_factory.create_pipe.assert_not_called()


async def test_composite_pipe_calls_single_step_with_correct_context(
    mock_pipe_factory, logger_factory, simple_step_configs, empty_pipeline_context
):
    mock_step = MagicMock()
    mock_step.process = AsyncMock(return_value=PipeResult.success(data={"value": "A"}))
    mock_pipe_factory.create_pipe.return_value = mock_step

    config = PipeConfig(
        id="composite",
        use="CompositePipe",
        params={"steps": [simple_step_configs[0]]},
    )
    composite = CompositePipe(pipe_factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    result = await composite.process(empty_pipeline_context)

    assert result.succeeded
    mock_pipe_factory.create_pipe.assert_called_once()
    call_args = mock_pipe_factory.create_pipe.call_args
    assert call_args[0][0] == simple_step_configs[0]
    assert call_args[0][1].parent_params is not None


async def test_composite_pipe_calls_multiple_steps_sequentially(
    mock_pipe_factory, logger_factory, simple_step_configs, empty_pipeline_context
):
    mock_steps: list[MagicMock] = []
    for index, _ in enumerate(simple_step_configs):
        mock_step = MagicMock()
        mock_step.process = AsyncMock(return_value=PipeResult.success(data={"value": chr(ALPHABET_START + index)}))
        mock_steps.append(mock_step)

    mock_pipe_factory.create_pipe.side_effect = mock_steps

    config = PipeConfig(id="composite", use="CompositePipe", params={"steps": simple_step_configs})
    composite = CompositePipe(pipe_factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    result = await composite.process(empty_pipeline_context)

    assert result.succeeded
    assert mock_pipe_factory.create_pipe.call_count == len(simple_step_configs)
    for mock_step in mock_steps:
        mock_step.process.assert_called_once()


async def test_composite_pipe_returns_union_of_results(
    mock_pipe_factory, logger_factory, simple_step_configs, empty_pipeline_context
):
    mock_step1 = MagicMock()
    mock_step1.process = AsyncMock(return_value=PipeResult.success(message="step1", data={"key1": "val1"}))
    mock_step2 = MagicMock()
    mock_step2.process = AsyncMock(return_value=PipeResult.success(message="step2", data={"key2": "val2"}))

    mock_pipe_factory.create_pipe.side_effect = [mock_step1, mock_step2]

    config = PipeConfig(id="composite", use="CompositePipe", params={"steps": simple_step_configs[:2]})
    composite = CompositePipe(pipe_factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    result = await composite.process(empty_pipeline_context)

    assert result.succeeded
    assert result.data == {"key1": "val1", "key2": "val2"}
    assert "step1" in result.message
    assert "step2" in result.message
