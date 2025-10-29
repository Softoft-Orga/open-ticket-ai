from typing import Any, ClassVar

import pytest
from pydantic import BaseModel

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


class ConcretePipeParams(BaseModel):
    value: str = "default"
    count: int = 0


class ConcretePipeForTesting(Pipe[ConcretePipeParams]):
    ParamsModel: ClassVar[type[BaseModel]] = ConcretePipeParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self.process_called = False

    async def _process(self, _: PipeContext) -> PipeResult:
        self.process_called = True
        return PipeResult.success(message="processed", data={"result": self._params.value})


@pytest.fixture
def pipe_config() -> PipeConfig:
    return PipeConfig(
        id="test_pipe",
        use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting",
        params={"value": "test_value", "count": 42},
    )


@pytest.fixture
def minimal_pipe_config() -> PipeConfig:
    return PipeConfig(id="minimal_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={})


@pytest.fixture
def test_pipe(pipe_config: PipeConfig, logger_factory: LoggerFactory) -> ConcretePipeForTesting:
    return ConcretePipeForTesting(config=pipe_config, logger_factory=logger_factory)


@pytest.fixture
def pipe_with_dependencies(logger_factory: LoggerFactory) -> ConcretePipeForTesting:
    config = PipeConfig(
        id="dependent_pipe",
        use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting",
        params={},
    )
    return ConcretePipeForTesting(config=config, logger_factory=logger_factory)


@pytest.fixture
def pipe_with_should_run_false(logger_factory: LoggerFactory) -> ConcretePipeForTesting:
    config = PipeConfig(id="disabled_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={})
    return ConcretePipeForTesting(config=config, logger_factory=logger_factory)


class TestPipeInitialization:
    def test_pipe_initialization_with_dict_params(self, pipe_config: PipeConfig, logger_factory: LoggerFactory):
        pipe = ConcretePipeForTesting(config=pipe_config, logger_factory=logger_factory)

        assert pipe._params.value == "test_value"
        assert pipe._params.count == 42

    def test_pipe_initialization_with_default_params(
        self, minimal_pipe_config: PipeConfig, logger_factory: LoggerFactory
    ):
        pipe = ConcretePipeForTesting(config=minimal_pipe_config, logger_factory=logger_factory)

        assert pipe._params.value == "default"
        assert pipe._params.count == 0

    def test_pipe_validates_params_as_pydantic_model(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="test_pipe",
            use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting",
            params={"value": "test", "count": 5},
        )
        pipe = ConcretePipeForTesting(config=config, logger_factory=logger_factory)

        assert isinstance(pipe._params, ConcretePipeParams)
        assert pipe._params.value == "test"
        assert pipe._params.count == 5


class TestPipeProcess:
    async def test_process_calls_process_when_should_run_true(
        self, test_pipe: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        result = await test_pipe.process(empty_pipeline_context)

        assert test_pipe.process_called
        assert result.succeeded
        assert not result.was_skipped
        assert result.message == "processed"
        assert result.data == {"result": "test_value"}
