import asyncio
import datetime
from datetime import timedelta
from unittest.mock import patch

import pytest
from otai_base.pipes.interval_trigger_pipe import IntervalTrigger, IntervalTriggerParams
from pydantic import ValidationError

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


@pytest.fixture
def empty_context() -> PipeContext:
    return PipeContext(pipe_results={}, params={})


def create_trigger_config(interval: float, **kwargs: bool | list[str]) -> PipeConfig:
    return PipeConfig(
        id="test_interval_trigger",
        use="open_ticket_ai.otai_base.pipes.interval_trigger_pipe.IntervalTrigger",
        params={"interval": interval},
        **kwargs,
    )


class TestIntervalTriggerInitialization:
    @pytest.mark.parametrize(
        "interval,expected",
        [
            (0.1, timedelta(seconds=0.1)),
            (0, timedelta(0)),
            (86400, timedelta(days=1)),
        ],
    )
    def test_initialization_with_valid_intervals(
        self, interval: float, expected: timedelta, logger_factory: LoggerFactory
    ):
        config = create_trigger_config(interval)
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        assert trigger._params.interval == expected
        assert isinstance(trigger.last_time_fired, datetime.datetime)
        assert trigger.last_time_fired.tzinfo == datetime.UTC

    @pytest.mark.parametrize(
        "params,error_type",
        [
            ({}, ValidationError),
            ({"interval": "invalid"}, ValidationError),
        ],
    )
    def test_initialization_errors(self, params: dict, error_type: type, logger_factory: LoggerFactory):
        config = PipeConfig(
            id="test_trigger",
            use="open_ticket_ai.otai_base.pipes.interval_trigger_pipe.IntervalTrigger",
            params=params,
        )
        with pytest.raises(error_type):
            IntervalTrigger(config=config, logger_factory=logger_factory)

    def test_params_model(self):
        assert IntervalTrigger.ParamsModel == IntervalTriggerParams


class TestIntervalTriggerBehavior:
    async def test_trigger_cycle_with_mocked_time(self, logger_factory: LoggerFactory, empty_context: PipeContext):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
        config = create_trigger_config(0.1)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

            result = await trigger.process(empty_context)
            assert not result.succeeded
            assert result.message == "Interval not reached yet."

            mock_datetime.now.return_value = initial_time + timedelta(seconds=0.11)
            result = await trigger.process(empty_context)
            assert result.succeeded
            assert trigger.last_time_fired == initial_time + timedelta(seconds=0.11)

            mock_datetime.now.return_value = initial_time + timedelta(seconds=0.15)
            result = await trigger.process(empty_context)
            assert not result.succeeded

    async def test_zero_interval_always_succeeds(self, logger_factory: LoggerFactory, empty_context: PipeContext):
        config = create_trigger_config(0)
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        for _ in range(3):
            result = await trigger.process(empty_context)
            assert result.succeeded

    async def test_negative_interval_succeeds(self, logger_factory: LoggerFactory, empty_context: PipeContext):
        config = create_trigger_config(-1)
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        result = await trigger.process(empty_context)
        assert result.succeeded

    async def test_real_time_interval(self, logger_factory: LoggerFactory, empty_context: PipeContext):
        config = create_trigger_config(0.001)
        trigger = IntervalTrigger(config=config, logger_factory=logger_factory)

        result = await trigger.process(empty_context)
        assert not result.succeeded

        await asyncio.sleep(0.002)
        result = await trigger.process(empty_context)
        assert result.succeeded
