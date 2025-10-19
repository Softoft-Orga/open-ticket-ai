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
def mock_pipe_factory(logger_factory: LoggerFactory) -> MagicMock:
    factory = MagicMock(spec=PipeFactory)

    def render_pipe_side_effect(pipe_config: PipeConfig, context: PipeContext) -> Pipe:
        return TrackingPipe(config=pipe_config, logger_factory=logger_factory, pipe_context=context)

    factory.render_pipe.side_effect = render_pipe_side_effect
    return factory


@pytest.fixture
def composite_pipe_with_empty_steps(mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory) -> CompositePipe:
    config = PipeConfig(
        id="composite_empty",
        use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
        params={},
        steps=[],
    )
    return CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)


@pytest.fixture
def composite_pipe_with_none_steps(
    mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory
) -> CompositePipe:
    config = PipeConfig(
        id="composite_none",
        use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
        params={},
        steps=None,
    )
    return CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)


@pytest.fixture
def composite_pipe_with_single_step(
    mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory
) -> CompositePipe:
    step_config = PipeConfig(
        id="step1",
        use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
        params={"value": "step1_value"},
    )
    config = PipeConfig(
        id="composite_single",
        use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
        params={},
        steps=[step_config],
    )
    return CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)


@pytest.fixture
def composite_pipe_with_multiple_steps(
    mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory
) -> CompositePipe:
    step1_config = PipeConfig(
        id="step1",
        use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
        params={"value": "step1_value"},
    )
    step2_config = PipeConfig(
        id="step2",
        use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
        params={"value": "step2_value"},
    )
    step3_config = PipeConfig(
        id="step3",
        use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
        params={"value": "step3_value"},
    )
    config = PipeConfig(
        id="composite_multiple",
        use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
        params={},
        steps=[step1_config, step2_config, step3_config],
    )
    return CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)


@pytest.fixture(autouse=True)
def reset_tracking():
    TrackingPipe.reset_tracking()
    yield
    TrackingPipe.reset_tracking()


class TestCompositePipeEmptySteps:
    async def test_empty_steps_list_returns_success_with_empty_data(
        self, composite_pipe_with_empty_steps: CompositePipe, empty_pipeline_context: PipeContext
    ):
        result = await composite_pipe_with_empty_steps.process(empty_pipeline_context)

        assert result.succeeded
        assert not result.was_skipped
        assert result.data == {}

    async def test_none_steps_returns_success_with_empty_data(
        self, composite_pipe_with_none_steps: CompositePipe, empty_pipeline_context: PipeContext
    ):
        result = await composite_pipe_with_none_steps.process(empty_pipeline_context)

        assert result.succeeded
        assert not result.was_skipped
        assert result.data == {}


class TestCompositePipeSingleStep:
    async def test_single_step_executes(
        self, composite_pipe_with_single_step: CompositePipe, empty_pipeline_context: PipeContext
    ):
        result = await composite_pipe_with_single_step.process(empty_pipeline_context)

        assert result.succeeded
        assert TrackingPipe.execution_order == ["step1"]
        assert result.data == {"value": "step1_value", "id": "step1"}

    async def test_single_step_context_parent_is_set(
        self, composite_pipe_with_single_step: CompositePipe, empty_pipeline_context: PipeContext
    ):
        await composite_pipe_with_single_step.process(empty_pipeline_context)

        assert len(TrackingPipe.context_snapshots) == 1
        step_context = TrackingPipe.context_snapshots[0]
        assert step_context.parent is not None
        assert isinstance(step_context.parent, dict)


class TestCompositePipeMultipleSteps:
    async def test_multiple_steps_execute_sequentially(
        self, composite_pipe_with_multiple_steps: CompositePipe, empty_pipeline_context: PipeContext
    ):
        result = await composite_pipe_with_multiple_steps.process(empty_pipeline_context)

        assert result.succeeded
        assert TrackingPipe.execution_order == ["step1", "step2", "step3"]

    async def test_multiple_steps_all_receive_context(
        self, composite_pipe_with_multiple_steps: CompositePipe, empty_pipeline_context: PipeContext
    ):
        await composite_pipe_with_multiple_steps.process(empty_pipeline_context)

        assert len(TrackingPipe.context_snapshots) == 3
        for snapshot in TrackingPipe.context_snapshots:
            assert snapshot.parent is not None
            assert isinstance(snapshot.parent, dict)

    async def test_multiple_steps_result_combines_all_data(
        self, composite_pipe_with_multiple_steps: CompositePipe, empty_pipeline_context: PipeContext
    ):
        result = await composite_pipe_with_multiple_steps.process(empty_pipeline_context)

        assert result.data == {"value": "step3_value", "id": "step3"}


class TestCompositePipeContextPropagation:
    async def test_context_includes_previous_results(
        self, mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory, empty_pipeline_context: PipeContext
    ):
        step1_config = PipeConfig(
            id="step1",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": "A"},
        )
        step2_config = PipeConfig(
            id="step2",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": "B"},
        )
        config = PipeConfig(
            id="composite_context_test",
            use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
            params={},
            steps=[step1_config, step2_config],
        )
        composite_pipe = CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

        await composite_pipe.process(empty_pipeline_context)

        assert len(TrackingPipe.context_snapshots) == 2
        step1_context = TrackingPipe.context_snapshots[0]
        step2_context = TrackingPipe.context_snapshots[1]

        assert step1_context.params == {}

        assert "value" in step2_context.params
        assert step2_context.params["value"] == "A"
        assert "id" in step2_context.params
        assert step2_context.params["id"] == "step1"

    async def test_context_accumulates_multiple_results(
        self, mock_pipe_factory: PipeFactory, logger_factory: LoggerFactory, empty_pipeline_context: PipeContext
    ):
        step1_config = PipeConfig(
            id="step1",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": "first"},
        )
        step2_config = PipeConfig(
            id="step2",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": "second"},
        )
        step3_config = PipeConfig(
            id="step3",
            use="tests.unit.base.pipes.test_composite_pipe.TrackingPipe",
            params={"value": "third"},
        )
        config = PipeConfig(
            id="composite_accumulate_test",
            use="open_ticket_ai.base.pipes.composite_pipe.CompositePipe",
            params={},
            steps=[step1_config, step2_config, step3_config],
        )
        composite_pipe = CompositePipe(factory=mock_pipe_factory, config=config, logger_factory=logger_factory)

        await composite_pipe.process(empty_pipeline_context)

        step3_context = TrackingPipe.context_snapshots[2]

        assert step3_context.params["value"] == "second"
        assert step3_context.params["id"] == "step2"
