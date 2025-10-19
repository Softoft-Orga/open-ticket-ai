import datetime
from datetime import timedelta
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from open_ticket_ai.base.pipes.interval_trigger_pipe import IntervalTrigger, IntervalTriggerParams
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


@pytest.fixture
def interval_trigger_config() -> PipeConfig:
    return PipeConfig(
        id="test_interval_trigger",
        use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
        params={"interval": 0.1},
    )


@pytest.fixture
def small_interval_config() -> PipeConfig:
    return PipeConfig(
        id="small_interval_trigger",
        use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
        params={"interval": 0.01},
    )


@pytest.fixture
def large_interval_config() -> PipeConfig:
    return PipeConfig(
        id="large_interval_trigger",
        use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
        params={"interval": 86400},
    )


@pytest.fixture
def zero_interval_config() -> PipeConfig:
    return PipeConfig(
        id="zero_interval_trigger",
        use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
        params={"interval": 0},
    )


@pytest.fixture
def empty_context() -> PipeContext:
    return PipeContext(pipe_results={}, params={})


class TestIntervalTriggerInitialization:
    def test_initialization_with_valid_interval(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory
    ):
        trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

        assert trigger._params.interval == timedelta(seconds=0.1)
        assert isinstance(trigger.last_time_fired, datetime.datetime)
        assert trigger.last_time_fired.tzinfo == datetime.UTC

    def test_initialization_with_small_interval(self, small_interval_config: PipeConfig, logger_factory: LoggerFactory):
        trigger = IntervalTrigger(config=small_interval_config, logger_factory=logger_factory)

        assert trigger._params.interval == timedelta(seconds=0.01)

    def test_initialization_with_large_interval(self, large_interval_config: PipeConfig, logger_factory: LoggerFactory):
        trigger = IntervalTrigger(config=large_interval_config, logger_factory=logger_factory)

        assert trigger._params.interval == timedelta(seconds=86400)

    def test_initialization_with_zero_interval(self, zero_interval_config: PipeConfig, logger_factory: LoggerFactory):
        trigger = IntervalTrigger(config=zero_interval_config, logger_factory=logger_factory)

        assert trigger._params.interval == timedelta(0)

    def test_initialization_with_missing_params_raises_error(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="missing_params_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={},
        )

        with pytest.raises(ValidationError):
            IntervalTrigger(config=config, logger_factory=logger_factory)

    def test_initialization_with_invalid_interval_type_raises_error(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="invalid_interval_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": "not a timedelta"},
        )

        with pytest.raises(ValidationError):
            IntervalTrigger(config=config, logger_factory=logger_factory)

    def test_params_model_is_interval_trigger_params(self):
        assert IntervalTrigger.get_params_model() == IntervalTriggerParams


class TestIntervalTriggerBehavior:
    async def test_trigger_fails_before_interval_elapses(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

        result = await trigger.process(empty_context)

        assert not result.succeeded
        assert result.message == "Interval not reached yet."
        assert not result.was_skipped

    async def test_trigger_succeeds_after_interval_with_mocked_time(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
        after_interval = initial_time + timedelta(seconds=0.11)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

            mock_datetime.now.return_value = after_interval
            result = await trigger.process(empty_context)

            assert result.succeeded
            assert result.message == ""
            assert not result.was_skipped

    async def test_trigger_fails_again_after_success_until_next_interval(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
        after_first_interval = initial_time + timedelta(seconds=0.11)
        after_short_delay = after_first_interval + timedelta(seconds=0.05)
        after_second_interval = after_first_interval + timedelta(seconds=0.11)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

            mock_datetime.now.return_value = after_first_interval
            result1 = await trigger.process(empty_context)
            assert result1.succeeded

            mock_datetime.now.return_value = after_short_delay
            result2 = await trigger.process(empty_context)
            assert not result2.succeeded
            assert result2.message == "Interval not reached yet."

            mock_datetime.now.return_value = after_second_interval
            result3 = await trigger.process(empty_context)
            assert result3.succeeded

    async def test_trigger_with_zero_interval_always_succeeds(
        self, zero_interval_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        trigger = IntervalTrigger(config=zero_interval_config, logger_factory=logger_factory)

        result1 = await trigger.process(empty_context)
        assert result1.succeeded

        result2 = await trigger.process(empty_context)
        assert result2.succeeded

        result3 = await trigger.process(empty_context)
        assert result3.succeeded

    async def test_trigger_updates_last_time_fired_on_success(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
        after_interval = initial_time + timedelta(seconds=0.11)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

            initial_last_time_fired = trigger.last_time_fired
            assert initial_last_time_fired == initial_time

            mock_datetime.now.return_value = after_interval
            await trigger.process(empty_context)

            assert trigger.last_time_fired == after_interval

    async def test_trigger_does_not_update_last_time_fired_on_failure(
        self, interval_trigger_config: PipeConfig, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
        before_interval = initial_time + timedelta(seconds=0.05)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            trigger = IntervalTrigger(config=interval_trigger_config, logger_factory=logger_factory)

            initial_last_time_fired = trigger.last_time_fired

            mock_datetime.now.return_value = before_interval
            result = await trigger.process(empty_context)

            assert not result.succeeded
            assert trigger.last_time_fired == initial_last_time_fired


class TestIntervalTriggerEdgeCases:
    async def test_trigger_with_real_small_interval(
        self, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        config = PipeConfig(
            id="real_small_interval",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": 0.001},
        )
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        result1 = await trigger.process(empty_context)
        assert not result1.succeeded

        import asyncio
        await asyncio.sleep(0.002)

        result2 = await trigger.process(empty_context)
        assert result2.succeeded

    async def test_trigger_respects_should_run_condition_false(
        self, logger_factory: LoggerFactory, empty_context: PipeContext
    ):
        config = PipeConfig(
            id="conditional_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": 0.001},
            if_=False,
        )
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        result = await trigger.process(empty_context)

        assert not result.succeeded
        assert result.was_skipped

    async def test_trigger_respects_dependencies(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="dependent_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": 0.1},
            depends_on=["dependency1"],
        )
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        empty_context = PipeContext(pipe_results={}, params={})
        result = await trigger.process(empty_context)

        assert not result.succeeded
        assert result.was_skipped

        context_with_dep = empty_context.with_pipe_result("dependency1", PipeResult.success())
        result2 = await trigger.process(context_with_dep)

        assert not result2.succeeded
        assert not result2.was_skipped
        assert result2.message == "Interval not reached yet."


class TestIntervalTriggerWithNegativeInterval:
    def test_negative_interval_initialization(self, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="negative_interval_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": -1},
        )

        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        assert trigger._params.interval == timedelta(seconds=-1)

    async def test_negative_interval_behavior(self, logger_factory: LoggerFactory, empty_context: PipeContext):
        config = PipeConfig(
            id="negative_interval_trigger",
            use="open_ticket_ai.base.pipes.interval_trigger_pipe.IntervalTrigger",
            params={"interval": -1},
        )
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        result = await trigger.process(empty_context)
        assert result.succeeded
