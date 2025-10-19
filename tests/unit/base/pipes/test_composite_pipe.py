from typing import Any, ClassVar
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.pipes.composite_pipe import CompositePipe
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class TrackingPipeParams(BaseModel):
    value: str = "default"


class TrackingPipe(Pipe[TrackingPipeParams]):
    execution_order: ClassVar[list[str]] = []
    context_snapshots: ClassVar[list[PipeContext]] = []

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return TrackingPipeParams

    async def _process(self, context: PipeContext) -> PipeResult:
        TrackingPipe.execution_order.append(self._config.id)
        TrackingPipe.context_snapshots.append(context)
        return PipeResult.success(data={"value": self._params.value, "id": self._config.id})

    @classmethod
    def reset_tracking(cls) -> None:
        cls.execution_order = []
        cls.context_snapshots = []


@pytest.fixture
def step_configs() -> list[PipeConfig]:
    return [
        PipeConfig(
            id=f"step{i}",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": f"value{i}"},
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def mock_pipe_factory(logger_factory: LoggerFactory) -> MagicMock:
    factory = MagicMock(spec=PipeFactory)
    factory.render_pipe.side_effect = lambda cfg, ctx: TrackingPipe(
        config=cfg, logger_factory=logger_factory, pipe_context=ctx
    )
    return factory


@pytest.fixture
def create_composite_pipe(mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory):
    def _create(steps: list[PipeConfig] | None) -> CompositePipe:
        config = PipeConfig(
            id="composite",
            use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
            params={},
            steps=steps,
        )
        return CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

    return _create


@pytest.fixture(autouse=True)
def reset_tracking():
    TrackingPipe.reset_tracking()
    yield
    TrackingPipe.reset_tracking()


async def test_empty_steps_returns_success(create_composite_pipe, empty_pipeline_context: PipeContext):
    for steps in [[], None]:
        result = await create_composite_pipe(steps).process(empty_pipeline_context)
        assert result.succeeded and not result.was_skipped and result.data == {}


async def test_single_step_execution_and_context_parent(
    create_composite_pipe, step_configs, empty_pipeline_context: PipeContext
):
    result = await create_composite_pipe([step_configs[0]]).process(empty_pipeline_context)

    assert result.succeeded
    assert TrackingPipe.execution_order == ["step1"]
    assert result.data == {"value": "value1", "id": "step1"}
    assert len(TrackingPipe.context_snapshots) == 1
    assert TrackingPipe.context_snapshots[0].parent is not None


async def test_multiple_steps_execute_sequentially(
    create_composite_pipe, step_configs, empty_pipeline_context: PipeContext
):
    result = await create_composite_pipe(step_configs).process(empty_pipeline_context)

    assert result.succeeded
    assert TrackingPipe.execution_order == ["step1", "step2", "step3"]
    assert all(s.parent is not None for s in TrackingPipe.context_snapshots)


async def test_context_propagates_previous_results(
    create_composite_pipe, step_configs, empty_pipeline_context: PipeContext
):
    await create_composite_pipe(step_configs[:2]).process(empty_pipeline_context)

    step1_context, step2_context = TrackingPipe.context_snapshots
    assert step1_context.params == {}
    assert step2_context.params == {"value": "value1", "id": "step1"}
