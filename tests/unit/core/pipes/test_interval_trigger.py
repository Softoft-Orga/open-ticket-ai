import asyncio
import datetime
from datetime import timedelta
from unittest.mock import patch

import pytest
from open_ticket_ai.pipes.interval_trigger_pipe import IntervalTrigger

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext


@pytest.fixture
def empty_context() -> PipeContext:
    return PipeContext.empty()


class TestIntervalTriggerInitialization:
    @pytest.mark.parametrize(
        "interval,expected",
        [
            (0.1, timedelta(seconds=0.1)),
            (0, timedelta(0)),
            (86400, timedelta(days=1)),
        ],
    )
    def test_initialization_with_valid_intervals(self, interval: float, expected: timedelta):
        trigger = IntervalTrigger(pipe_id="test", interval_seconds=interval)
        assert trigger._interval == expected
        assert isinstance(trigger._last_fired, datetime.datetime)
        assert trigger._last_fired.tzinfo == datetime.UTC


class TestIntervalTriggerBehavior:
    async def test_trigger_cycle_with_mocked_time(self, empty_context: PipeContext):
        initial_time = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)

        with patch("open_ticket_ai.pipes.interval_trigger_pipe.datetime") as mock_datetime:
            mock_datetime.datetime.now.return_value = initial_time
            mock_datetime.UTC = datetime.UTC
            mock_datetime.timedelta = datetime.timedelta
            trigger = IntervalTrigger(pipe_id="test", interval_seconds=0.1)

            result = await trigger.process(empty_context)
            assert not result.succeeded

            mock_datetime.datetime.now.return_value = initial_time + timedelta(seconds=0.11)
            result = await trigger.process(empty_context)
            assert result.succeeded

            mock_datetime.datetime.now.return_value = initial_time + timedelta(seconds=0.15)
            result = await trigger.process(empty_context)
            assert not result.succeeded

    async def test_zero_interval_always_succeeds(self, empty_context: PipeContext):
        trigger = IntervalTrigger(pipe_id="test", interval_seconds=0)
        for _ in range(3):
            result = await trigger.process(empty_context)
            assert result.succeeded

    async def test_negative_interval_succeeds(self, empty_context: PipeContext):
        trigger = IntervalTrigger(pipe_id="test", interval_seconds=-1)
        result = await trigger.process(empty_context)
        assert result.succeeded

    async def test_real_time_interval(self, empty_context: PipeContext):
        trigger = IntervalTrigger(pipe_id="test", interval_seconds=0.001)
        result = await trigger.process(empty_context)
        assert not result.succeeded

        await asyncio.sleep(0.002)
        result = await trigger.process(empty_context)
        assert result.succeeded
