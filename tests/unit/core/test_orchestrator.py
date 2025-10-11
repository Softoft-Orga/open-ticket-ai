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

    assert config.runners[0].pipe.id == "demo"
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

    assert config.runners[0].id == "test-runner"
    assert config.runners[0].pipe.id == "demo"
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


def test_orchestrator_config_with_defaults_applies_to_runners() -> None:
    raw = {
        "defaults": {
            "pipe": {"id": "default-pipe", "use": "some.default:Pipe"},
        },
        "runners": [
            {
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
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.defaults is not None
    assert config.runners[0].pipe.id == "default-pipe"
    assert config.runners[0].pipe.use == "some.default:Pipe"


def test_orchestrator_config_with_defaults_can_be_overridden() -> None:
    raw = {
        "defaults": {
            "pipe": {"id": "default-pipe"},
        },
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "specific-pipe"},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].pipe.id == "specific-pipe"


def test_orchestrator_config_with_defaults_params_merge() -> None:
    raw = {
        "defaults": {
            "pipe": {
                "id": "default-pipe",
                "params": {"default_param": "default_value", "shared_param": "default_shared"},
            },
        },
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"params": {"runner_param": "runner_value", "shared_param": "runner_shared"}},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].pipe.params["default_param"] == "default_value"
    assert config.runners[0].pipe.params["runner_param"] == "runner_value"
    assert config.runners[0].pipe.params["shared_param"] == "runner_shared"


def test_orchestrator_config_with_defaults_settings_applied_and_overridden() -> None:
    raw = {
        "defaults": {
            "settings": {
                "timeout": "30s",
                "priority": 5,
                "retry_scope": "job",
            },
        },
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "test-pipe"},
                "settings": {
                    "timeout": "60s",
                    "priority": 15,
                },
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].settings.timeout == "60s"
    assert config.runners[0].settings.priority == 15
    assert config.runners[0].settings.retry_scope == "job"


def test_orchestrator_config_with_defaults_nested_settings() -> None:
    raw = {
        "defaults": {
            "settings": {
                "concurrency": {
                    "max_workers": 5,
                    "when_exhausted": "drop",
                },
                "retry": {
                    "attempts": 5,
                    "delay": "10s",
                    "backoff_factor": 3.0,
                },
            },
        },
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "test-pipe"},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].settings.concurrency is not None
    assert config.runners[0].settings.concurrency.when_exhausted == "drop"
    assert config.runners[0].settings.retry is not None
    assert config.runners[0].settings.retry.attempts == 5


def test_orchestrator_config_without_defaults() -> None:
    raw = {
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "test-pipe"},
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

    assert config.defaults is None
    assert config.runners[0].pipe.id == "test-pipe"


def test_orchestrator_config_with_defaults_multiple_runners() -> None:
    raw = {
        "defaults": {
            "pipe": {"use": "some.default:Pipe", "params": {"default_key": "default_value"}},
            "settings": {"timeout": "30s", "priority": 5},
        },
        "runners": [
            {
                "triggers": [
                    {
                        "id": "interval-trigger-1",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "pipe": {"id": "pipe-1"},
            },
            {
                "triggers": [
                    {
                        "id": "interval-trigger-2",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 20},
                    }
                ],
                "pipe": {"id": "pipe-2", "params": {"runner_key": "runner_value"}},
            },
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 2
    assert config.runners[0].pipe.use == "some.default:Pipe"
    assert config.runners[1].pipe.params["runner_key"] == "runner_value"
    assert config.runners[1].settings.timeout == "30s"
