import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import BaseModel

# Ensure the package root is on the import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from open_ticket_ai.src.core.pipeline.pipeline import Pipeline
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.status import PipelineStatus
from open_ticket_ai.src.core.config.config_models import PipelineConfig, ScheduleConfig


class DummyData(BaseModel):
    value: int = 0


class IncrementPipe:
    InputDataType = DummyData

    def __init__(self):
        self.config = SimpleNamespace(id="inc")

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        context.data.value += 1
        return context


class StopPipe:
    InputDataType = DummyData

    def __init__(self):
        self.config = SimpleNamespace(id="stop")

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        context.data.value += 1
        context.stop_pipeline()
        return context


class ErrorPipe:
    InputDataType = DummyData

    def __init__(self):
        self.config = SimpleNamespace(id="error")

    def process(self, context: PipelineContext[DummyData]) -> PipelineContext[DummyData]:
        raise RuntimeError("boom")


@pytest.fixture
def pipeline_config_factory():
    def _factory(pipes: list):
        return PipelineConfig(
            id="test_pipeline",
            schedule=ScheduleConfig(interval=1, unit="minutes"),
            pipes=[p.config.id for p in pipes],
        )

    return _factory


def test_execute_success(pipeline_config_factory):
    pipes = [IncrementPipe(), IncrementPipe()]
    pipeline = Pipeline(pipeline_config_factory(pipes), pipes)
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())

    result = pipeline.execute(context)

    assert result.data.value == 2
    assert result.meta_info.status == PipelineStatus.SUCCESS


def test_execute_stop(pipeline_config_factory):
    pipes = [IncrementPipe(), StopPipe(), IncrementPipe()]
    pipeline = Pipeline(pipeline_config_factory(pipes), pipes)
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())

    result = pipeline.execute(context)

    assert result.data.value == 2
    assert result.meta_info.status == PipelineStatus.STOPPED


def test_execute_error(pipeline_config_factory):
    pipes = [IncrementPipe(), ErrorPipe(), IncrementPipe()]
    pipeline = Pipeline(pipeline_config_factory(pipes), pipes)
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())

    result = pipeline.execute(context)

    assert result.data.value == 1
    assert result.meta_info.status == PipelineStatus.FAILED
    assert result.meta_info.failed_pipe == "ErrorPipe"
    assert "boom" in result.meta_info.error_message


def test_non_runnable_initial_status(pipeline_config_factory):
    pipes = [IncrementPipe()]
    pipeline = Pipeline(pipeline_config_factory(pipes), pipes)
    meta = MetaInfo(status=PipelineStatus.STOPPED)
    context = PipelineContext(data=DummyData(value=5), meta_info=meta)

    result = pipeline.execute(context)

    assert result.data.value == 5
    assert result.meta_info.status == PipelineStatus.STOPPED


def test_process_alias(pipeline_config_factory):
    pipes = [IncrementPipe()]
    pipeline = Pipeline(pipeline_config_factory(pipes), pipes)
    context = PipelineContext(data=DummyData(value=0), meta_info=MetaInfo())

    result = pipeline.process(context)

    assert result.data.value == 1
    assert result.meta_info.status == PipelineStatus.SUCCESS
