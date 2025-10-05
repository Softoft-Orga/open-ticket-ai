from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.pipeline import (
    Orchestrator,
    OrchestratorConfig,
)
from open_ticket_ai.core.pipeline.context import Context


def test_orchestrator_config_from_raw() -> None:
    raw = [
        {
            "run_every_milli_seconds": 1000,
            "pipe": {"id": "demo"},
        }
    ]

    config = OrchestratorConfig.from_raw(raw)

    assert len(config.runners) == 1
    assert config.runners[0].pipe["id"] == "demo"
    assert config.runners[0].interval_seconds == 1.0


def test_orchestrator_config_default_max_runners() -> None:
    raw = [
        {
            "run_every_milli_seconds": 1000,
            "pipe": {"id": "demo"},
        }
    ]

    config = OrchestratorConfig.from_raw(raw)

    assert config.max_runners == 100


def test_orchestrator_config_duplicate_pipe_ids_warning(caplog) -> None:
    raw = [
        {
            "run_every_milli_seconds": 1000,
            "pipe": {"id": "demo"},
        },
        {
            "run_every_milli_seconds": 2000,
            "pipe": {"id": "demo"},
        },
        {
            "run_every_milli_seconds": 3000,
            "pipe": {"id": "other"},
        },
    ]

    config = OrchestratorConfig.from_raw(raw)

    assert len(config.runners) == 3
    assert "Duplicate pipe IDs detected" in caplog.text
    assert "demo" in caplog.text


def test_orchestrator_config_empty() -> None:
    config = OrchestratorConfig.from_raw(None)
    
    assert len(config.runners) == 0
    assert config.max_runners == 100


@pytest.mark.asyncio
async def test_orchestrator_exceeds_max_runners() -> None:
    runners = [
        {"run_every_milli_seconds": 1000, "pipe": {"id": f"pipe_{i}"}}
        for i in range(150)
    ]
    
    config = RawOpenTicketAIConfig(orchestrator=runners)
    orchestrator = Orchestrator(config)
    
    with pytest.raises(ValueError, match="maximum allowed is 100"):
        await orchestrator.start()


@pytest.mark.asyncio
async def test_orchestrator_warning_near_max_runners(caplog) -> None:
    runners = [
        {"run_every_milli_seconds": 1000, "pipe": {"id": f"pipe_{i}"}}
        for i in range(85)
    ]
    
    config = RawOpenTicketAIConfig(orchestrator=runners)
    orchestrator = Orchestrator(config)
    
    with pytest.raises(Exception):
        await orchestrator.start()
    
    assert "approaching the maximum limit" in caplog.text


def test_orchestrator_starts_and_stops_runners() -> None:
    config = RawOpenTicketAIConfig(
        orchestrator=[{"run_every_milli_seconds": 10, "pipe": {"id": "demo"}}]
    )
    pipe_factory = MagicMock()
    process_mock = AsyncMock(return_value=Context())
    pipe_factory.create_pipe.return_value = SimpleNamespace(process=process_mock)

    orchestrator = Orchestrator(pipe_factory, config)

    orchestrator.run()
    try:
        time.sleep(0.05)
    finally:
        orchestrator.stop()

    assert pipe_factory.create_pipe.call_count >= 1
    assert process_mock.await_count >= 1
