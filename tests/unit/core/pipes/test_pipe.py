from typing import Any

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
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self.process_called = False

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return ConcretePipeParams

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
        depends_on=["pipe1", "pipe2"],
    )
    return ConcretePipeForTesting(config=config, logger_factory=logger_factory)


@pytest.fixture
def pipe_with_should_run_false(logger_factory: LoggerFactory) -> ConcretePipeForTesting:
    config = PipeConfig(
        id="disabled_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={}, if_=False
    )
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

    async def test_process_with_if_false_condition(
        self, pipe_with_should_run_false: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        result = await pipe_with_should_run_false.process(empty_pipeline_context)

        assert pipe_with_should_run_false.process_called
        assert result.succeeded

    async def test_process_with_unfulfilled_dependencies(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        result = await pipe_with_dependencies.process(empty_pipeline_context)

        assert pipe_with_dependencies.process_called
        assert result.succeeded


class TestPipeDependencies:
    async def test_dependencies_fulfilled_when_all_succeeded(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.success())

        result = await pipe_with_dependencies.process(context)

        assert pipe_with_dependencies.process_called
        assert result.succeeded

    async def test_dependencies_check_with_one_failed(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.failure("failed"))

        result = await pipe_with_dependencies.process(context)

        assert pipe_with_dependencies.process_called
        assert result.succeeded

    async def test_dependencies_check_with_one_skipped(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.skipped())

        result = await pipe_with_dependencies.process(context)

        assert pipe_with_dependencies.process_called
        assert result.succeeded

    async def test_dependencies_check_with_missing_dependency(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())

        result = await pipe_with_dependencies.process(context)

        assert pipe_with_dependencies.process_called
        assert result.succeeded


class TestPipeShouldRun:
    async def test_should_run_checks_if_condition(self, logger_factory: LoggerFactory):
        config_with_if_true = PipeConfig(
            id="test_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={}, if_=True
        )
        pipe = ConcretePipeForTesting(config=config_with_if_true, logger_factory=logger_factory)

        should_run = await pipe._should_run(PipeContext(pipe_results={}, params={}))
        assert should_run

    async def test_should_run_false_when_if_false(self, logger_factory: LoggerFactory):
        config_with_if_false = PipeConfig(
            id="test_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={}, if_=False
        )
        pipe = ConcretePipeForTesting(config=config_with_if_false, logger_factory=logger_factory)

        should_run = await pipe._should_run(PipeContext(pipe_results={}, params={}))
        assert not should_run

    async def test_should_run_with_string_condition(self, logger_factory: LoggerFactory):
        config_with_string_if = PipeConfig(
            id="test_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={}, if_="true"
        )
        pipe = ConcretePipeForTesting(config=config_with_string_if, logger_factory=logger_factory)

        should_run = await pipe._should_run(PipeContext(pipe_results={}, params={}))
        assert should_run

    def test_are_dependencies_fulfilled_returns_true_when_all_succeeded(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.success())

        fulfilled = pipe_with_dependencies._are_dependencies_fulfilled(context)
        assert fulfilled

    def test_are_dependencies_fulfilled_returns_false_when_one_failed(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.failure("failed"))

        fulfilled = pipe_with_dependencies._are_dependencies_fulfilled(context)
        assert not fulfilled

    def test_are_dependencies_fulfilled_returns_false_when_one_skipped(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())
        context = context.with_pipe_result("pipe2", PipeResult.skipped())

        fulfilled = pipe_with_dependencies._are_dependencies_fulfilled(context)
        assert not fulfilled

    def test_are_dependencies_fulfilled_returns_false_when_missing(
        self, pipe_with_dependencies: ConcretePipeForTesting, empty_pipeline_context: PipeContext
    ):
        context = empty_pipeline_context.with_pipe_result("pipe1", PipeResult.success())

        fulfilled = pipe_with_dependencies._are_dependencies_fulfilled(context)
        assert not fulfilled


class TestPipeConfig:
    def test_pipe_stores_config(self, test_pipe: ConcretePipeForTesting):
        assert test_pipe._config is not None
        assert test_pipe._config.id == "test_pipe"

    def test_pipe_config_with_dependencies(self, pipe_with_dependencies: ConcretePipeForTesting):
        assert pipe_with_dependencies._config.depends_on == ["pipe1", "pipe2"]

    def test_pipe_config_should_run_property(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="test_pipe", use="tests.unit.core.pipes.test_pipe.ConcretePipeForTesting", params={}, if_=False
        )
        pipe = ConcretePipeForTesting(config=config, logger_factory=logger_factory)

        assert pipe._config.should_run is False
