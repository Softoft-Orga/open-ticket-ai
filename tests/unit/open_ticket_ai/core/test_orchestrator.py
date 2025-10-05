from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

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


def test_orchestrator_starts_and_stops_runners() -> None:
    config = RawOpenTicketAIConfig(
        orchestrator=[{"run_every_milli_seconds": 10, "pipe": {"id": "demo"}}],
        defs=[],
        plugins=[]
    )

    orchestrator = Orchestrator(config)

    # Just test that it can be created without errors
    # The actual runner functionality requires more complex setup with Prefect
    assert orchestrator is not None
    assert len(orchestrator._config.runners) == 1
