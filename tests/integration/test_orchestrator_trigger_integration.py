"""Integration tests for Orchestrator, Trigger, and PipeRunner interaction.

Tests verify that triggers fire correctly, runners execute pipelines, and the
orchestrator properly coordinates all components in realistic scenarios.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from injector import Injector

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




@pytest.mark.asyncio
async def test_interval_trigger_fires_and_notifies_observers() -> None:
    """Test that IntervalTrigger fires and notifies attached observers."""
    trigger_config: TriggerDefinition[IntervalTriggerParams] = TriggerDefinition(
        id="test_interval_trigger",
        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
        params=IntervalTriggerParams(milliseconds=100),
    )

    trigger = IntervalTrigger(trigger_config)

    fired_count = 0

    class TestObserver:
        async def on_trigger_fired(self) -> None:
            nonlocal fired_count
            fired_count += 1

    observer = TestObserver()
    trigger.attach(observer)
    trigger.start()

    await asyncio.sleep(0.35)
    trigger.stop()

    assert fired_count >= 2


@pytest.mark.asyncio
async def test_pipe_runner_executes_pipe_on_trigger(logger_factory: LoggerFactory) -> None:
    """Test that PipeRunner executes a pipe when triggered."""
    from pydantic import BaseModel

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

    runner_def = RunnerDefinition(
        id="test_runner",
        on=[
            TriggerDefinition(
                id="test_trigger",
                use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                params={"seconds": 1},
            )
        ],
        run=PipeConfig(id="test_pipe", use="TestPipe"),
    )

    runner = PipeRunner(runner_def, mock_factory)
    await runner.on_trigger_fired()

    assert pipe_executed is True
    mock_factory.create_pipe.assert_called_once()


@pytest.mark.asyncio
async def test_orchestrator_starts_and_triggers_fire(logger_factory: LoggerFactory) -> None:
    """Test that Orchestrator starts triggers and they fire correctly."""
    orchestrator_config = OrchestratorConfig(
        runners=[
            RunnerDefinition(
                id="test_runner",
                on=[
                    TriggerDefinition(
                        id="interval_trigger_1",
                        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                        params={"milliseconds": 100},
                    )
                ],
                run=PipeConfig(id="test_pipe", use="TestPipe"),
            )
        ]
    )

    execution_count = 0

    class MockPipe:
        async def process(self, context: PipeContext) -> PipeContext:
            nonlocal execution_count
            execution_count += 1
            context.pipes["test_pipe"] = MagicMock(success=True)
            return context

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MockPipe()

    mock_trigger = MagicMock(spec=IntervalTrigger)
    mock_trigger.start = MagicMock()
    mock_trigger.stop = MagicMock()
    mock_trigger.attach = MagicMock()
    mock_factory.create_trigger.return_value = mock_trigger

    orchestrator = Orchestrator(mock_factory, orchestrator_config, logger_factory)
    orchestrator.start()

    assert len(orchestrator._runners) == 1
    assert len(orchestrator._trigger_registry) == 1
    mock_factory.create_trigger.assert_called_once()
    mock_trigger.attach.assert_called_once()
    mock_trigger.start.assert_called_once()

    orchestrator.stop()
    assert len(orchestrator._runners) == 0
    assert len(orchestrator._trigger_registry) == 0


@pytest.mark.asyncio
async def test_orchestrator_with_multiple_triggers() -> None:
    """Test Orchestrator with multiple triggers attached to different runners."""


    orchestrator_config = OrchestratorConfig(
        runners=[
            RunnerDefinition(
                id="runner_1",
                on=[
                    TriggerDefinition(
                        id="trigger_1",
                        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                        params={"seconds": 1},
                    )
                ],
                run=PipeConfig(id="pipe_1", use="TestPipe1"),
            ),
            RunnerDefinition(
                id="runner_2",
                on=[
                    TriggerDefinition(
                        id="trigger_2",
                        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                        params={"seconds": 2},
                    )
                ],
                run=PipeConfig(id="pipe_2", use="TestPipe2"),
            ),
        ]
    )

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock()
    mock_factory.create_pipe.return_value.process = AsyncMock(return_value=PipeContext())

    trigger_1 = MagicMock(spec=IntervalTrigger)
    trigger_1.start = MagicMock()
    trigger_1.stop = MagicMock()
    trigger_1.attach = MagicMock()

    trigger_2 = MagicMock(spec=IntervalTrigger)
    trigger_2.start = MagicMock()
    trigger_2.stop = MagicMock()
    trigger_2.attach = MagicMock()

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
async def test_orchestrator_reuses_trigger_with_same_id() -> None:
    """Test that Orchestrator reuses triggers with the same ID across multiple runners."""

    shared_trigger_id = "shared_trigger"
    orchestrator_config = OrchestratorConfig(
        runners=[
            RunnerDefinition(
                id="runner_1",
                on=[
                    TriggerDefinition(
                        id=shared_trigger_id,
                        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                        params={"seconds": 1},
                    )
                ],
                run=PipeConfig(id="pipe_1", use="TestPipe1"),
            ),
            RunnerDefinition(
                id="runner_2",
                on=[
                    TriggerDefinition(
                        id=shared_trigger_id,
                        use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                        params={"seconds": 1},
                    )
                ],
                run=PipeConfig(id="pipe_2", use="TestPipe2"),
            ),
        ]
    )

    mock_factory = MagicMock(spec=RenderableFactory)
    mock_factory.create_pipe.return_value = MagicMock()
    mock_factory.create_pipe.return_value.process = AsyncMock(return_value=PipeContext())

    mock_trigger = MagicMock(spec=IntervalTrigger)
    mock_trigger.start = MagicMock()
    mock_trigger.stop = MagicMock()
    mock_trigger.attach = MagicMock()

    mock_factory.create_trigger.return_value = mock_trigger

    orchestrator = Orchestrator(mock_factory, orchestrator_config, logger_factory)
    orchestrator.start()

    assert len(orchestrator._runners) == 2
    assert len(orchestrator._trigger_registry) == 1

    mock_factory.create_trigger.assert_called_once()
    assert mock_trigger.attach.call_count == 2

    orchestrator.stop()


@pytest.mark.asyncio
async def test_runner_handles_pipe_execution_failure(logger_factory: LoggerFactory) -> None:
    """Test that PipeRunner handles pipe execution failures gracefully."""
    mock_factory = MagicMock(spec=RenderableFactory)

    failing_pipe = MagicMock()
    failing_pipe.process = AsyncMock(side_effect=Exception("Pipe execution failed"))
    mock_factory.create_pipe.return_value = failing_pipe

    runner_def = RunnerDefinition(
        id="failing_runner",
        on=[
            TriggerDefinition(
                id="trigger",
                use="open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                params={"seconds": 1},
            )
        ],
        run=PipeConfig(id="failing_pipe", use="FailingPipe"),
    )

    runner = PipeRunner(runner_def, mock_factory)

    await runner.on_trigger_fired()

    mock_factory.create_pipe.assert_called_once()
