"""Integration tests for Orchestrator, Trigger, and PipeRunner interaction.

Tests verify that triggers fire correctly, runners execute pipelines, and the
orchestrator properly coordinates all components in realistic scenarios.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.triggers.interval_trigger import IntervalTrigger, IntervalTriggerParams
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator import Orchestrator
from open_ticket_ai.core.orchestration.orchestrator_config import (
    OrchestratorConfig,
    RunnerDefinition,
    TriggerDefinition,
)
from open_ticket_ai.core.orchestration.scheduled_runner import PipeRunner
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


def create_trigger_def(trigger_id: str, **params: int) -> TriggerDefinition[IntervalTriggerParams]:
    return TriggerDefinition[IntervalTriggerParams](
        id=trigger_id,
        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
        params=IntervalTriggerParams(**params),
    )


def create_mock_trigger() -> MagicMock:
    mock_trigger = MagicMock(spec=IntervalTrigger)
    mock_trigger.start = MagicMock()
    mock_trigger.stop = MagicMock()
    mock_trigger.attach = MagicMock()
    return mock_trigger


def create_runner_def(runner_id: str, trigger_id: str, pipe_id: str, **trigger_params: int) -> RunnerDefinition:
    return RunnerDefinition(
        id=runner_id,
        on=[create_trigger_def(trigger_id, **trigger_params)],
        run=PipeConfig(id=pipe_id, use=f"{pipe_id.title()}"),
    )


@pytest.mark.asyncio
async def test_interval_trigger_fires_and_notifies_observers(logger_factory: LoggerFactory) -> None:
    """Test that IntervalTrigger fires and notifies attached observers."""
    trigger = IntervalTrigger(create_trigger_def("test_interval_trigger", milliseconds=100), logger_factory)
    fired_count = 0

    class TestObserver:
        async def on_trigger_fired(self) -> None:
            nonlocal fired_count
            fired_count += 1

    trigger.attach(TestObserver())
    trigger.start()
    await asyncio.sleep(0.35)
    trigger.stop()

    assert fired_count >= 2


@pytest.mark.asyncio
async def test_pipe_runner_executes_pipe_on_trigger(logger_factory: LoggerFactory) -> None:
    """Test that PipeRunner executes a pipe when triggered."""
    pipe_executed = False

    class EmptyData(BaseModel):
        pass

    class TestPipe(Pipe[EmptyData]):
        async def _process(self) -> PipeResult[EmptyData]:
            nonlocal pipe_executed
            pipe_executed = True
            return PipeResult(success=True, failed=False, data=EmptyData())

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = TestPipe(PipeConfig(id="test_pipe", use="TestPipe"), logger_factory)

    runner = PipeRunner(create_runner_def("test_runner", "test_trigger", "test_pipe", seconds=1), mock_factory, logger_factory)
    await runner.on_trigger_fired()

    assert pipe_executed is True
    mock_factory.create_pipe.assert_called_once()


@pytest.mark.asyncio
async def test_orchestrator_starts_and_triggers_fire(logger_factory: LoggerFactory) -> None:
    """Test that Orchestrator starts triggers and they fire correctly."""
    orchestrator_config = OrchestratorConfig(
        runners=[create_runner_def("test_runner", "interval_trigger_1", "test_pipe", milliseconds=100)]
    )

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock(process=AsyncMock(return_value=PipeContext()))
    mock_factory.create_trigger.return_value = create_mock_trigger()

    orchestrator = Orchestrator(mock_factory, orchestrator_config, logger_factory)
    orchestrator.start()

    assert len(orchestrator._runners) == 1
    assert len(orchestrator._trigger_registry) == 1
    mock_factory.create_trigger.assert_called_once()

    orchestrator.stop()
    assert len(orchestrator._runners) == 0
    assert len(orchestrator._trigger_registry) == 0


@pytest.mark.asyncio
async def test_orchestrator_with_multiple_triggers(logger_factory: LoggerFactory) -> None:
    """Test Orchestrator with multiple triggers attached to different runners."""
    orchestrator_config = OrchestratorConfig(
        runners=[
            create_runner_def("runner_1", "trigger_1", "pipe_1", seconds=1),
            create_runner_def("runner_2", "trigger_2", "pipe_2", seconds=2),
        ]
    )

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock(process=AsyncMock(return_value=PipeContext()))

    trigger_1, trigger_2 = create_mock_trigger(), create_mock_trigger()
    mock_factory.create_trigger.side_effect = [trigger_1, trigger_2]

    orchestrator = Orchestrator(mock_factory, orchestrator_config, logger_factory)
    orchestrator.start()

    assert len(orchestrator._runners) == 2
    assert len(orchestrator._trigger_registry) == 2
    assert mock_factory.create_trigger.call_count == 2
    trigger_1.start.assert_called_once()
    trigger_2.start.assert_called_once()

    orchestrator.stop()


@pytest.mark.asyncio
async def test_orchestrator_reuses_trigger_with_same_id(logger_factory: LoggerFactory) -> None:
    """Test that Orchestrator reuses triggers with the same ID across multiple runners."""
    shared_trigger_id = "shared_trigger"
    orchestrator_config = OrchestratorConfig(
        runners=[
            create_runner_def("runner_1", shared_trigger_id, "pipe_1", seconds=1),
            create_runner_def("runner_2", shared_trigger_id, "pipe_2", seconds=1),
        ]
    )

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock(process=AsyncMock(return_value=PipeContext()))
    mock_factory.create_trigger.return_value = create_mock_trigger()

    orchestrator = Orchestrator(mock_factory, orchestrator_config, logger_factory)
    orchestrator.start()

    assert len(orchestrator._runners) == 2
    assert len(orchestrator._trigger_registry) == 1
    mock_factory.create_trigger.assert_called_once()
    assert mock_factory.create_trigger.return_value.attach.call_count == 2

    orchestrator.stop()


@pytest.mark.asyncio
async def test_runner_handles_pipe_execution_failure(logger_factory: LoggerFactory) -> None:
    """Test that PipeRunner handles pipe execution failures gracefully."""
    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock(process=AsyncMock(side_effect=Exception("Pipe execution failed")))

    runner = PipeRunner(create_runner_def("failing_runner", "trigger", "failing_pipe", seconds=1), mock_factory, logger_factory)
    await runner.on_trigger_fired()

    mock_factory.create_pipe.assert_called_once()
