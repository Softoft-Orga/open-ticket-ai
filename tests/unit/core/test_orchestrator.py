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


def test_orchestrator_config_with_params() -> None:
    raw = {
        "runners": [
            {
                "id": "test-runner-with-params",
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "demo"},
                "params": {
                    "concurrency": {
                        "max_workers": 5,
                        "when_exhausted": "wait",
                    },
                    "retry": {
                        "attempts": 5,
                        "delay": "10s",
                    },
                    "timeout": "30s",
                    "priority": 20,
                },
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 1
    assert config.runners[0].id == "test-runner-with-params"
    assert config.runners[0].params is not None
    assert config.runners[0].params.concurrency is not None
    assert config.runners[0].params.concurrency.max_workers == 5
    assert config.runners[0].params.concurrency.when_exhausted == "wait"
    assert config.runners[0].params.retry is not None
    assert config.runners[0].params.retry.attempts == 5
    assert config.runners[0].params.retry.delay == "10s"
    assert config.runners[0].params.timeout == "30s"
    assert config.runners[0].params.priority == 20

