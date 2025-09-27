"""
Pytest tests for the core pipeline components including Pipeline, Pipe, PipelineContext, MetaInfo, and PipelineStatus.
"""

import pytest

pytest.importorskip("pydantic")
from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import PipelineConfig, ProvidableConfig, ScheduleConfig

# Assuming the following imports are correct based on your project structure
# You may need to adjust them based on your PYTHONPATH
from open_ticket_ai.core.pipeline.context import MetaInfo, PipelineContext, PipelineStatus
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipeline import Pipeline

# --- Test Data and Dummy Implementations ---


class DummyData(BaseModel):
    """A simple Pydantic model for data used in tests."""

    value: int


class IncrementPipe(Pipe[ProvidableConfig, DummyData, DummyData]):
    """A dummy pipe that increments the value in the context data."""

    InputDataType = DummyData
    OutputDataType = DummyData

    def __init__(self, config: ProvidableConfig = None):
        if config is None:
            config = ProvidableConfig(id="increment_pipe", provider_key="increment_pipe")
        super().__init__(config)

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        print("IncrementPipe processing")
        print("IncrementPipe input:", context.data)
        context.data.value += 1
        return context


class StopPipe(Pipe[ProvidableConfig, DummyData, DummyData]):
    """A dummy pipe that increments a value and then stops the pipeline."""

    InputDataType = DummyData
    OutputDataType = DummyData

    def __init__(self, config: ProvidableConfig = None):
        if config is None:
            config = ProvidableConfig(id="stop_pipe", provider_key="stop_pipe")
        super().__init__(config)

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        context.data.value += 1
        context.stop_pipeline()
        return context


class ErrorPipe(Pipe[ProvidableConfig, DummyData, DummyData]):
    """A dummy pipe that always raises an exception."""

    InputDataType = DummyData
    OutputDataType = DummyData

    def __init__(self, config: ProvidableConfig = None):
        if config is None:
            config = ProvidableConfig(id="error_pipe", provider_key="error_pipe")
        super().__init__(config)

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        raise RuntimeError("This is a test error from ErrorPipe.")


# --- Pytest Fixtures ---


@pytest.fixture
def pipeline_config_factory():
    """A factory fixture to create PipelineConfig instances."""

    def _factory(pipes: list[Pipe]):
        # The actual pipe_ids in config don't matter as much when we inject instances,
        # but we'll keep it consistent.
        pipe_ids = [p.config.id for p in pipes]
        return PipelineConfig(
            id="test_pipeline",
            run_every_seconds=ScheduleConfig(interval=10, unit="minutes"),
            pipes=pipe_ids,
        )

    return _factory


# --- Test Cases ---


def test_pipeline_status_enum():
    """Tests that the PipelineStatus enum has the correct members."""
    assert hasattr(PipelineStatus, "RUNNING")
    assert hasattr(PipelineStatus, "SUCCESS")
    assert hasattr(PipelineStatus, "STOPPED")
    assert hasattr(PipelineStatus, "FAILED")
    assert len(PipelineStatus) == 4


def test_meta_info_defaults():
    """Tests that MetaInfo initializes with correct default values."""
    meta = MetaInfo()
    assert meta.status == PipelineStatus.RUNNING
    assert meta.error_message is None
    assert meta.failed_pipe is None


def test_meta_info_custom_values():
    """Tests creating a MetaInfo object with non-default values."""
    meta = MetaInfo(status=PipelineStatus.FAILED, error_message="Something went wrong", failed_pipe="ErrorPipe")
    assert meta.status == PipelineStatus.FAILED
    assert meta.error_message == "Something went wrong"
    assert meta.failed_pipe == "ErrorPipe"


def test_pipeline_context_creation():
    """Tests the basic creation of a PipelineContext."""
    data = DummyData(value=42)
    meta = MetaInfo()
    context = PipelineContext(data=data, meta_info=meta)
    assert context.data.value == 42
    assert context.meta_info.status == PipelineStatus.RUNNING


def test_context_stop_pipeline():
    """Tests the stop_pipeline method in PipelineContext."""
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())
    assert context.meta_info.status == PipelineStatus.RUNNING
    context.stop_pipeline()
    assert context.meta_info.status == PipelineStatus.STOPPED


def test_pipeline_successful_execution(pipeline_config_factory):
    """Tests a pipeline that should execute all its pipes successfully."""
    pipes = [IncrementPipe(), IncrementPipe(), IncrementPipe()]
    config = pipeline_config_factory(pipes)
    pipeline = Pipeline(config, pipes)
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())

    result_context = pipeline.execute(context)

    assert result_context.data.value == 3
    assert result_context.meta_info.status == PipelineStatus.SUCCESS
    assert result_context.meta_info.error_message is None
    assert result_context.meta_info.failed_pipe is None


def test_pipeline_stops_execution_on_request(pipeline_config_factory):
    """Tests that a pipeline correctly stops when a pipe requests it."""
    pipes = [IncrementPipe(), StopPipe(), IncrementPipe()]
    config = pipeline_config_factory(pipes)
    pipeline = Pipeline(config, pipes)
    context = PipelineContext(data=DummyData(value=10), meta_info=MetaInfo())

    result_context = pipeline.execute(context)

    # The value should be 12 because the first two pipes run, but the third does not.
    assert result_context.data.value == 12
    assert result_context.meta_info.status == PipelineStatus.STOPPED
    assert result_context.meta_info.failed_pipe is None


def test_pipeline_handles_errors(pipeline_config_factory):
    """Tests that a pipeline handles exceptions from a pipe and sets the FAILED status."""
    pipes = [IncrementPipe(), ErrorPipe(), IncrementPipe()]
    config = pipeline_config_factory(pipes)
    pipeline = Pipeline(config, pipes)
    context = PipelineContext(data=DummyData(value=20), meta_info=MetaInfo())

    result_context = pipeline.execute(context)

    # The value should be 21 because only the first pipe runs successfully.
    assert result_context.data.value == 21
    assert result_context.meta_info.status == PipelineStatus.FAILED
    assert result_context.meta_info.failed_pipe == "ErrorPipe"
    assert "This is a test error from ErrorPipe" in result_context.meta_info.error_message


@pytest.mark.parametrize(
    "initial_status",
    [
        PipelineStatus.FAILED,
        PipelineStatus.STOPPED,
    ],
)
def test_pipeline_does_not_run_with_non_runnable_initial_status(pipeline_config_factory, initial_status):
    """Tests that the pipeline does not execute if the initial context status is not runnable."""
    pipes = [IncrementPipe()]
    config = pipeline_config_factory(pipes)
    pipeline = Pipeline(config, pipes)
    meta = MetaInfo(status=initial_status)
    context = PipelineContext(data=DummyData(value=50), meta_info=meta)

    result_context = pipeline.execute(context)

    # The value should not change
    assert result_context.data.value == 50
    assert result_context.meta_info.status == initial_status
