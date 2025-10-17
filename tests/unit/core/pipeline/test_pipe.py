from __future__ import annotations

from typing import Any

import pytest
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.renderable.renderable import Renderable

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.logging.logging_iface import LoggerFactory

pytestmark = [pytest.mark.unit]


class MinimalPipeParams(StrictBaseModel):
    pass


class MinimalConcretePipe(Pipe[MinimalPipeParams]):
    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, **kwargs: Any) -> None:
        Renderable.__init__(self, config, logger_factory, **kwargs)
        self._config: PipeConfig = PipeConfig.model_validate(config.model_dump())
        self._logger = logger_factory.create(self.__class__.__name__)

    @staticmethod
    def get_params_model() -> type[StrictBaseModel]:
        return MinimalPipeParams


@pytest.mark.asyncio
async def test_process_returns_skipped_by_default(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    config = PipeConfig(id="test_pipe", use="test.MinimalConcretePipe")
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(empty_pipeline_context)

    assert result.was_skipped
    assert result.succeeded
    assert not result.has_failed()


@pytest.mark.asyncio
@pytest.mark.parametrize("should_run", [True, False, "True", "False"])
async def test_process_with_should_run_false(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
    should_run: bool | str,
) -> None:
    config = PipeConfig(id="test_pipe", use="test.MinimalConcretePipe", if_=should_run)
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(empty_pipeline_context)

    if should_run in [False, "False"]:
        assert result.was_skipped
    else:
        assert result.was_skipped or not result.has_failed()


@pytest.mark.asyncio
async def test_process_with_dependencies_not_fulfilled(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="test_pipe",
        use="test.MinimalConcretePipe",
        depends_on=["dependency_pipe_1", "dependency_pipe_2"],
    )
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(empty_pipeline_context)

    assert result.was_skipped
    assert result.succeeded


@pytest.mark.asyncio
async def test_process_with_dependencies_fulfilled(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    context_with_results = empty_pipeline_context.with_pipe_result(
        "dependency_pipe_1", PipeResult.success()
    ).with_pipe_result("dependency_pipe_2", PipeResult.success())

    config = PipeConfig(
        id="test_pipe",
        use="test.MinimalConcretePipe",
        depends_on=["dependency_pipe_1", "dependency_pipe_2"],
    )
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(context_with_results)

    assert result.was_skipped
    assert result.succeeded


@pytest.mark.asyncio
async def test_process_with_one_dependency_not_fulfilled(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    context_with_partial_results = empty_pipeline_context.with_pipe_result("dependency_pipe_1", PipeResult.success())

    config = PipeConfig(
        id="test_pipe",
        use="test.MinimalConcretePipe",
        depends_on=["dependency_pipe_1", "dependency_pipe_2"],
    )
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(context_with_partial_results)

    assert result.was_skipped


@pytest.mark.asyncio
async def test_process_with_dependency_skipped(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    context_with_skipped = empty_pipeline_context.with_pipe_result("dependency_pipe_1", PipeResult.skipped())

    config = PipeConfig(
        id="test_pipe",
        use="test.MinimalConcretePipe",
        depends_on=["dependency_pipe_1"],
    )
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(context_with_skipped)

    assert result.was_skipped


@pytest.mark.asyncio
async def test_process_with_dependency_failed(
    logger_factory: LoggerFactory,
    empty_pipeline_context: PipeContext,
) -> None:
    context_with_failure = empty_pipeline_context.with_pipe_result(
        "dependency_pipe_1", PipeResult.failure("Test failure")
    )

    config = PipeConfig(
        id="test_pipe",
        use="test.MinimalConcretePipe",
        depends_on=["dependency_pipe_1"],
    )
    pipe = MinimalConcretePipe(config=config, logger_factory=logger_factory)

    result = await pipe.process(context_with_failure)

    assert result.was_skipped
