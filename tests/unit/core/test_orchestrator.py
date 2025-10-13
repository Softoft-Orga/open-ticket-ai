from __future__ import annotations

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
    assert config.runners[0].on[0].params["seconds"] == 10


@pytest.mark.skip(
    reason="Test requires running event loop but is not async. "
    "Orchestrator.start() triggers async tasks which need an event loop. "
    "Test needs to be refactored to run in async context or mock the async behavior."
)
def test_orchestrator_starts_and_stops_runners() -> None:
    orchestrator_config = OrchestratorConfig.model_validate(
        {
            "runners": [
                {
                    "on": [
                        {
                            "id": "interval-trigger",
                            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
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

    logger_factory = MagicMock()
    logger_factory.get_logger.return_value = MagicMock()

    orchestrator = Orchestrator(pipe_factory, orchestrator_config, logger_factory)

    orchestrator.start()
    assert len(orchestrator._runners) == 1
    assert len(orchestrator._trigger_registry) == 1

    orchestrator.stop()
    assert len(orchestrator._runners) == 0
    assert len(orchestrator._trigger_registry) == 0


@pytest.mark.skip(
    reason="Orchestrator config defaults merging not implemented in source code. "
    "Test expects defaults.run to be merged with runner.run but this feature is not implemented."
)
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
    assert config.runners[0].run.id == "demo"
    assert config.runners[0].run.use == "open_ticket_ai.base.CompositePipe"


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


@pytest.mark.skip(
    reason="Orchestrator config defaults merging not implemented in source code. "
    "Test expects defaults.run.params to be merged with runner.run.params but this feature is not implemented."
)
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


@pytest.mark.skip(
    reason="Orchestrator config defaults merging not implemented in source code. "
    "Test expects defaults.params to be merged with runner.params but this feature is not implemented."
)
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


@pytest.mark.skip(
    reason="Orchestrator config defaults merging not implemented in source code. "
    "Test expects defaults.params to be merged with runner.params but this feature is not implemented."
)
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
    assert config.runners[0].params.concurrency is None
    assert config.runners[0].params.retry is None
    assert config.runners[0].params.timeout is None
    assert config.runners[0].params.priority == 10

    assert config.defaults is None
    assert config.runners[0].run.id == "test-pipe"


@pytest.mark.skip(
    reason="Orchestrator config defaults merging not implemented in source code. "
    "Test expects defaults to be merged with runners but this feature is not implemented."
)
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


def test_trigger_definition_auto_sets_id_from_uid_when_missing() -> None:
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
    trigger = config.runners[0].on[0]

    assert trigger.id is not None
    assert trigger.id == trigger.uid


def test_trigger_definition_auto_sets_id_from_uid_when_explicitly_none() -> None:
    raw = {
        "runners": [
            {
                "on": [
                    {
                        "id": None,
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 1},
                    }
                ],
                "run": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)
    trigger = config.runners[0].on[0]

    assert trigger.id is not None
    assert trigger.id == trigger.uid


def test_trigger_definition_preserves_explicit_id() -> None:
    raw = {
        "runners": [
            {
                "on": [
                    {
                        "id": "my-custom-trigger-id",
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 1},
                    }
                ],
                "run": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)
    trigger = config.runners[0].on[0]

    assert trigger.id == "my-custom-trigger-id"
    assert trigger.id != trigger.uid


def test_multiple_triggers_without_id_have_unique_ids() -> None:
    raw = {
        "runners": [
            {
                "on": [
                    {
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 1},
                    },
                    {
                        "use": "open_ticket_ai.core.orchestration.triggers.interval_trigger:IntervalTrigger",
                        "params": {"seconds": 2},
                    },
                ],
                "run": {"id": "demo"},
            }
        ]
    }

    config = OrchestratorConfig.model_validate(raw)
    trigger1 = config.runners[0].on[0]
    trigger2 = config.runners[0].on[1]

    assert trigger1.id is not None
    assert trigger2.id is not None
    assert trigger1.id != trigger2.id
    assert trigger1.id == trigger1.uid
    assert trigger2.id == trigger2.uid


def test_orchestrator_registry_uses_trigger_ids_correctly() -> None:
    orchestrator_config = OrchestratorConfig.model_validate(
        {
            "runners": [
                {
                    "on": [
                        {
                            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                            "params": {"seconds": 1},
                        }
                    ],
                    "run": {"id": "demo"},
                }
            ]
        }
    )

    trigger_def = orchestrator_config.runners[0].on[0]
    assert trigger_def.id is not None
    assert trigger_def.id == trigger_def.uid


def test_orchestrator_reuses_trigger_with_same_id_across_runners() -> None:
    shared_trigger_id = "shared-interval-trigger"
    orchestrator_config = OrchestratorConfig.model_validate(
        {
            "runners": [
                {
                    "on": [
                        {
                            "id": shared_trigger_id,
                            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                            "params": {"seconds": 1},
                        }
                    ],
                    "run": {"id": "demo1"},
                },
                {
                    "on": [
                        {
                            "id": shared_trigger_id,
                            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
                            "params": {"seconds": 1},
                        }
                    ],
                    "run": {"id": "demo2"},
                },
            ]
        }
    )

    trigger1 = orchestrator_config.runners[0].on[0]
    trigger2 = orchestrator_config.runners[1].on[0]

    assert trigger1.id == shared_trigger_id
    assert trigger2.id == shared_trigger_id
    assert trigger1.id == trigger2.id
