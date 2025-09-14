"""Tests for :mod:`ticket_queue_updater` pipe."""

from __future__ import annotations

from typing import Any

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import (
    HFLocalAIInferenceServiceOutput,
)
from open_ticket_ai.src.base.pipe_implementations.ticket_queue_updater.models import (
    TicketQueueUpdaterConfig,
)
from open_ticket_ai.src.base.pipe_implementations.ticket_queue_updater.ticket_queue_updater import (
    TicketQueueUpdater,
)
from open_ticket_ai.src.base.pipe_implementations.empty_data_model import (
    EmptyDataModel,
)
from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import (
    TicketSystemAdapter,
)
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    UnifiedQueue,
    UnifiedTicket,
)


class DummyTicketSystem(TicketSystemAdapter):
    """Minimal ticket system adapter used for testing."""

    def __init__(self) -> None:  # pragma: no cover - simple passthrough
        super().__init__(SystemConfig(id="sys", provider_key="dummy"))
        self.updated: list[tuple[str, UnifiedTicket]] = []

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        self.updated.append((ticket_id, updates))
        return True

    async def find_tickets(self, criteria: Any) -> list[UnifiedTicket]:  # pragma: no cover - not used
        return []

    async def find_first_ticket(self, criteria: Any) -> UnifiedTicket | None:  # pragma: no cover - not used
        return None


def _make_context(prediction: str, confidence: float, ticket_id: str) -> PipelineContext:
    return PipelineContext(
        data=HFLocalAIInferenceServiceOutput(
            prediction=prediction,
            confidence=confidence,
            ticket=UnifiedTicket(id=ticket_id),
        )
    )


def _make_updater(**cfg_overrides: Any) -> tuple[TicketQueueUpdater, DummyTicketSystem]:
    cfg = TicketQueueUpdaterConfig(
        id="updater",
        provider_key="updater",
        confidence_threshold=0.8,
        low_confidence_queue="General",
        ticket_system_value2model_values={"Sales": "sales", "Support": "support"},
        **cfg_overrides,
    )
    system = DummyTicketSystem()
    return TicketQueueUpdater(cfg, system), system


def test_updates_queue_when_confident() -> None:
    updater, system = _make_updater()
    context = _make_context("sales", 0.9, "42")

    result = updater.process(context)

    assert system.updated[0][0] == "42"
    assert system.updated[0][1].queue == UnifiedQueue(name="Sales")
    assert isinstance(result.data, EmptyDataModel)


def test_uses_low_confidence_queue_when_below_threshold() -> None:
    updater, system = _make_updater()
    context = _make_context("sales", 0.5, "99")

    updater.process(context)

    assert system.updated[0][1].queue == UnifiedQueue(name="General")


def test_no_update_when_no_data() -> None:
    updater, system = _make_updater()

    updater.process(PipelineContext())

    assert system.updated == []

