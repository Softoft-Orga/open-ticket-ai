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


def test_orchestrator_config_with_defaults_pipe_id() -> None:
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
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.defaults is not None
    assert config.defaults.pipe.id == "default-pipe"
    assert len(config.runners) == 1
    assert config.runners[0].pipe.id == "default-pipe"


def test_orchestrator_config_with_defaults_pipe_use() -> None:
    raw = {
        "defaults": {
            "pipe": {"use": "some.default:Pipe"},
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
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.defaults is not None
    assert config.defaults.pipe.use == "some.default:Pipe"
    assert len(config.runners) == 1
    assert config.runners[0].pipe.use == "some.default:Pipe"


def test_orchestrator_config_with_defaults_override() -> None:
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

    assert config.defaults is not None
    assert config.defaults.pipe.id == "default-pipe"
    assert len(config.runners) == 1
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

    assert config.defaults is not None
    assert config.defaults.pipe.id == "default-pipe"
    assert config.defaults.pipe.params == {"default_param": "default_value", "shared_param": "default_shared"}
    assert len(config.runners) == 1
    assert config.runners[0].pipe.id == "default-pipe"
    assert config.runners[0].pipe.params["default_param"] == "default_value"
    assert config.runners[0].pipe.params["runner_param"] == "runner_value"
    assert config.runners[0].pipe.params["shared_param"] == "runner_shared"


def test_orchestrator_config_with_defaults_settings() -> None:
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
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.defaults is not None
    assert config.defaults.settings.timeout == "30s"
    assert config.defaults.settings.priority == 5
    assert config.defaults.settings.retry_scope == "job"
    assert len(config.runners) == 1
    assert config.runners[0].settings.timeout == "30s"
    assert config.runners[0].settings.priority == 5
    assert config.runners[0].settings.retry_scope == "job"


def test_orchestrator_config_with_defaults_settings_override() -> None:
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

    assert config.defaults is not None
    assert len(config.runners) == 1
    assert config.runners[0].settings.timeout == "60s"
    assert config.runners[0].settings.priority == 15
    assert config.runners[0].settings.retry_scope == "job"


def test_orchestrator_config_with_defaults_concurrency() -> None:
    raw = {
        "defaults": {
            "settings": {
                "concurrency": {
                    "max_workers": 5,
                    "when_exhausted": "drop",
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

    assert config.defaults is not None
    assert config.defaults.settings.concurrency is not None
    assert config.defaults.settings.concurrency.max_workers == 5
    assert config.defaults.settings.concurrency.when_exhausted == "drop"
    assert len(config.runners) == 1
    assert config.runners[0].settings.concurrency is not None
    assert config.runners[0].settings.concurrency.max_workers == 5
    assert config.runners[0].settings.concurrency.when_exhausted == "drop"


def test_orchestrator_config_with_defaults_retry() -> None:
    raw = {
        "defaults": {
            "settings": {
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

    assert config.defaults is not None
    assert config.defaults.settings.retry is not None
    assert config.defaults.settings.retry.attempts == 5
    assert config.defaults.settings.retry.delay == "10s"
    assert config.defaults.settings.retry.backoff_factor == 3.0
    assert len(config.runners) == 1
    assert config.runners[0].settings.retry is not None
    assert config.runners[0].settings.retry.attempts == 5
    assert config.runners[0].settings.retry.delay == "10s"
    assert config.runners[0].settings.retry.backoff_factor == 3.0


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

    assert config.defaults is None
    assert len(config.runners) == 1
    assert config.runners[0].pipe.id == "test-pipe"
    assert config.runners[0].settings.priority == 10


def test_orchestrator_config_with_empty_defaults() -> None:
    raw = {
        "defaults": {},
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

    assert config.defaults is not None
    assert len(config.runners) == 1
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

    assert config.defaults is not None
    assert len(config.runners) == 2

    assert config.runners[0].pipe.id == "pipe-1"
    assert config.runners[0].pipe.use == "some.default:Pipe"
    assert config.runners[0].pipe.params["default_key"] == "default_value"
    assert config.runners[0].settings.timeout == "30s"
    assert config.runners[0].settings.priority == 5

    assert config.runners[1].pipe.id == "pipe-2"
    assert config.runners[1].pipe.use == "some.default:Pipe"
    assert config.runners[1].pipe.params["default_key"] == "default_value"
    assert config.runners[1].pipe.params["runner_key"] == "runner_value"
    assert config.runners[1].settings.timeout == "30s"
    assert config.runners[1].settings.priority == 5

