from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.orchestration.orchestrator import Orchestrator
from open_ticket_ai.core.orchestration.orchestrator_config import OrchestratorConfig

from open_ticket_ai.core.pipeline.pipe_context import PipeContext


def test_orchestrator_config_from_raw_legacy() -> None:
    raw = {
        "runners": [
            {
                "on": [
                    {
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 1},
                    }
                ],
                "run": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].run.id == "demo"
    assert config.runners[0].on[0].use == "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger"
    assert config.runners[0].on[0].params["seconds"] == 1


def test_orchestrator_config_from_raw_new_format() -> None:
    raw = {
        "runners": [
            {
                "id": "test-runner",
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].id == "test-runner"
    assert config.runners[0].run.id == "demo"
    assert config.runners[0].on[0].params.seconds == 10


def test_orchestrator_starts_and_stops_runners() -> None:
    orchestrator_config = OrchestratorConfig.model_validate(
        {
            "runners": [
                {
                    "on": [
                        {
                            "id": "interval-trigger",
                            "use": "open_ticket_ai.base.interval_trigger:IntervalTrigger",
                            "params": {"seconds": 1},
                        }
                    ],
                    "run": {"id": "demo"},
                }
            ]
        }
    )
    pipe_factory = MagicMock()
    process_mock = AsyncMock(return_value=PipeContext())
    pipe_factory.create_pipe.return_value = SimpleNamespace(process=process_mock)

    orchestrator = Orchestrator(pipe_factory, orchestrator_config)

    orchestrator.start()
    assert len(orchestrator._runners) == 1
    assert len(orchestrator._trigger_registry) == 1

    orchestrator.stop()
    assert len(orchestrator._runners) == 0
    assert len(orchestrator._trigger_registry) == 0


def test_orchestrator_config_with_defaults_applies_to_runners() -> None:
    raw = {
        "defaults": {
            "run": {"id": "default-pipe", "use": "some.default:Pipe"},
        },
        "runners": [
            {
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "demo"},
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
    assert config.runners[0].run.id == "default-pipe"
    assert config.runners[0].run.use == "some.default:Pipe"


def test_orchestrator_config_with_defaults_can_be_overridden() -> None:
    raw = {
        "defaults": {
            "run": {"id": "default-pipe"},
        },
        "runners": [
            {
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "specific-pipe"},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].run.id == "specific-pipe"


def test_orchestrator_config_with_defaults_params_merge() -> None:
    raw = {
        "defaults": {
            "run": {
                "id": "default-pipe",
                "params": {"default_param": "default_value", "shared_param": "default_shared"},
            },
        },
        "runners": [
            {
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"params": {"runner_param": "runner_value", "shared_param": "runner_shared"}},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].run.params["default_param"] == "default_value"
    assert config.runners[0].run.params["runner_param"] == "runner_value"
    assert config.runners[0].run.params["shared_param"] == "runner_shared"


def test_orchestrator_config_with_defaults_settings_applied_and_overridden() -> None:
    raw = {
        "defaults": {
            "params": {
                "timeout": "30s",
                "priority": 5,
                "retry_scope": "job",
            },
        },
        "runners": [
            {
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "test-pipe"},
                "params": {
                    "timeout": "60s",
                    "priority": 15,
                },
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].params.timeout == "60s"
    assert config.runners[0].params.priority == 15
    assert config.runners[0].params.retry_scope == "job"


def test_orchestrator_config_with_defaults_nested_settings() -> None:
    raw = {
        "defaults": {
            "params": {
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
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "test-pipe"},
            }
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert config.runners[0].params.concurrency is not None
    assert config.runners[0].params.concurrency.when_exhausted == "drop"
    assert config.runners[0].params.retry is not None
    assert config.runners[0].params.retry.attempts == 5


def test_orchestrator_config_without_defaults() -> None:
    raw = {
        "runners": [
            {
                "id": "test-runner-with-params",
                "on": [
                    {
                        "id": "interval-trigger",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "test-pipe"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 1
    assert config.runners[0].id == "test-runner-with-params"
    assert config.runners[0].params is not None
    assert config.runners[0].params.concurrency is not None
    assert config.runners[0].params.concurrency.max_workers == 1
    assert config.runners[0].params.concurrency.when_exhausted == "wait"
    assert config.runners[0].params.retry is not None
    assert config.runners[0].params.retry.attempts == 3
    assert config.runners[0].params.retry.delay == "5s"
    assert config.runners[0].params.timeout is None
    assert config.runners[0].params.priority == 10

    assert config.defaults is None
    assert config.runners[0].run.id == "test-pipe"


def test_orchestrator_config_with_defaults_multiple_runners() -> None:
    raw = {
        "defaults": {
            "run": {"use": "some.default:Pipe", "params": {"default_key": "default_value"}},
            "params": {"timeout": "30s", "priority": 5},
        },
        "runners": [
            {
                "on": [
                    {
                        "id": "interval-trigger-1",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 10},
                    }
                ],
                "run": {"id": "pipe-1"},
            },
            {
                "on": [
                    {
                        "id": "interval-trigger-2",
                        "use": "apscheduler.triggers.interval:IntervalTrigger",
                        "params": {"seconds": 20},
                    }
                ],
                "run": {"id": "pipe-2", "params": {"runner_key": "runner_value"}},
            },
        ],
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 2
    assert config.runners[0].run.use == "some.default:Pipe"
    assert config.runners[1].run.params["runner_key"] == "runner_value"
    assert config.runners[1].params.timeout == "30s"
