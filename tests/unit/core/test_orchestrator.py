from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from open_ticket_ai.core.pipeline import (
    Orchestrator,
    OrchestratorConfig,
)
from open_ticket_ai.core.pipeline.context import Context


def test_orchestrator_config_from_raw() -> None:
    raw = {
        "runners":
            [
                {
                    "run_every_milli_seconds": 1000,
                    "pipe": {"id": "demo"},
                }
            ]
    }

    config = OrchestratorConfig.model_validate(raw)

    assert len(config.runners) == 1
    assert config.runners[0].pipe["id"] == "demo"
    assert config.runners[0].interval_seconds == 1.0


import pytest


@pytest.mark.asyncio
async def test_orchestrator_starts_and_stops_runners() -> None:
    orchestrator_config = OrchestratorConfig.model_validate({
        "runners": [
            {
                "run_every_milli_seconds": 10,
                "pipe": {"id": "demo"},
            }
        ]
    })
    pipe_factory = MagicMock()
    process_mock = AsyncMock(return_value=Context())
    pipe_factory.create_pipe.return_value = SimpleNamespace(process=process_mock)

    orchestrator = Orchestrator(pipe_factory, orchestrator_config)

    # Test that start and stop work without errors
    await orchestrator.start()
    # Verify the scheduler is running
    assert orchestrator._scheduler.running

    await orchestrator.stop()
    # Give scheduler time to shut down
    await asyncio.sleep(0.01)
    # Verify the scheduler is stopped
    assert not orchestrator._scheduler.running
