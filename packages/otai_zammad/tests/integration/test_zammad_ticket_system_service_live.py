from __future__ import annotations

import os
from uuid import uuid4

import httpx
import pytest

from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import StdlibLoggerFactory
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)
from otai_zammad.zammad_ticket_system_service import ZammadTicketsystemService

pytestmark = [pytest.mark.integration]

BASE_URL = os.getenv("OTAI_ZAMMAD_TEST_URL", "http://18.156.167.59/")
TOKEN = (os.getenv("OTAI_ZAMMAD_TEST_TOKEN") or "").strip()

if not TOKEN:
    pytest.skip("OTAI_ZAMMAD_TEST_TOKEN is required for live Zammad integration tests", allow_module_level=True)


@pytest.fixture
async def zammad_service() -> ZammadTicketsystemService:
    headers = {
        "Authorization": f"Token token={TOKEN}",
        "Accept": "application/json",
    }
    client = httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30.0)
    config = InjectableConfig(
        id="integration-test",
        params={
            "base_url": BASE_URL,
            "access_token": TOKEN,
        },
    )
    logger_factory = StdlibLoggerFactory(LoggingConfig(level="INFO"))
    service = ZammadTicketsystemService(client=client, config=config, logger_factory=logger_factory)
    try:
        yield service
    finally:
        await service.aclose()
        await client.aclose()


@pytest.mark.asyncio
async def test_zammad_ticket_workflow(zammad_service: ZammadTicketsystemService) -> None:
    unique_subject = f"Integration Test Ticket {uuid4()}"
    initial_body = "Integration test ticket body"

    created_ticket_id = await zammad_service.create_ticket(
        UnifiedTicket(subject=unique_subject, body=initial_body)
    )
    assert created_ticket_id.isdigit()

    retrieved = await zammad_service.get_ticket(created_ticket_id)
    assert retrieved is not None
    assert retrieved.subject == unique_subject
    assert retrieved.body == initial_body

    tickets = await zammad_service.find_tickets(TicketSearchCriteria(limit=100))
    assert any(ticket.id == created_ticket_id for ticket in tickets)

    follow_up_body = "Integration follow-up note"
    updated_subject = f"{unique_subject} - Updated"
    update_payload = UnifiedTicket(
        subject=updated_subject,
        notes=[UnifiedNote(subject="Follow up", body=follow_up_body)],
    )
    assert await zammad_service.update_ticket(created_ticket_id, update_payload)

    updated_ticket = await zammad_service.get_ticket(created_ticket_id)
    assert updated_ticket is not None
    assert updated_ticket.subject == updated_subject
    assert updated_ticket.notes is not None
    assert any(note.body == follow_up_body for note in updated_ticket.notes)

    standalone_note_body = "Integration standalone note"
    standalone_note = UnifiedNote(subject="Standalone", body=standalone_note_body)
    assert await zammad_service.add_note(created_ticket_id, standalone_note)

    final_ticket = await zammad_service.get_ticket(created_ticket_id)
    assert final_ticket is not None
    assert final_ticket.notes is not None
    assert any(note.body == standalone_note_body for note in final_ticket.notes)
