from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.pipeline.orchestrator import Orchestrator
from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext


def test_orchestrator_config_from_raw_legacy() -> None:
    raw = {
        "runners": [
            {
                "run_every_milli_seconds": 1000,
                "pipe": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 1
    assert config.runners[0].pipe.id == "demo"
    assert len(config.runners[0].triggers) == 1
    assert config.runners[0].triggers[0].use == "apscheduler.triggers.interval:IntervalTrigger"
    assert config.runners[0].triggers[0].params["seconds"] == 1


def test_orchestrator_config_from_raw_new_format() -> None:
    raw = {
        "runners": [
            {
                "id": "test-runner",
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 1
    assert config.runners[0].id == "test-runner"
    assert config.runners[0].pipe.id == "demo"
    assert len(config.runners[0].triggers) == 1
    assert config.runners[0].triggers[0].id == "interval-trigger"
    assert config.runners[0].triggers[0].use == "apscheduler.triggers.interval:IntervalTrigger"
    assert config.runners[0].triggers[0].params["seconds"] == 10


@pytest.mark.asyncio
async def test_orchestrator_starts_and_stops_runners() -> None:
    orchestrator_config = OrchestratorConfig.model_validate(
        {
            "runners": [
                {
                    "triggers": [
                        {
                            "id": "interval-trigger",
                            "use": "apscheduler.triggers.interval:IntervalTrigger",
                            "params": {"seconds": 1},
                        }
                    ],
                    "pipe": {"id": "demo"},
                }
            ]
        }
    )
    pipe_factory = MagicMock()
    process_mock = AsyncMock(return_value=PipeContext())
    pipe_factory.create_pipe.return_value = SimpleNamespace(process=process_mock)

    orchestrator = Orchestrator(pipe_factory, orchestrator_config)

    orchestrator.start()
    assert orchestrator._scheduler.running

    orchestrator.stop()
    await asyncio.sleep(0.01)
    assert not orchestrator._scheduler.running
