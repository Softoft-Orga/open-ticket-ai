# packages/otai_zammad/tests/integration/test_zammad_ticket_system_service_live.py
from __future__ import annotations

import os
from typing import Any, AsyncGenerator
from uuid import uuid4

import httpx
import pytest

from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import StdlibLoggerFactory
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket, UnifiedEntity,
)
from otai_zammad.zammad_ticket_system_service import ZammadTicketsystemService

pytestmark = [pytest.mark.integration]

BASE_URL = os.getenv("OTAI_ZAMMAD_TEST_URL", "http://18.156.167.59/").rstrip("/") + "/"
TOKEN = (os.getenv("OTAI_ZAMMAD_TEST_TOKEN") or "").strip()

if not TOKEN:
    pytest.skip("OTAI_ZAMMAD_TEST_TOKEN is required for live Zammad integration tests", allow_module_level=True)


@pytest.fixture
async def zammad_service() -> AsyncGenerator[ZammadTicketsystemService, Any]:
    headers = {
        "Authorization": f"Token token={TOKEN}",
        "Accept": "application/json",
    }
    client = httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30.0)
    config = InjectableConfig(
        id="integration-test",
        params={"base_url": BASE_URL, "access_token": TOKEN},
    )
    logger_factory = StdlibLoggerFactory(LoggingConfig(level="DEBUG"))
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
    print(f"\n=== Creating ticket with subject: {unique_subject}")
    created_ticket_id = await zammad_service.create_ticket(
        UnifiedTicket(
            subject=unique_subject,
            body=initial_body,
            queue=UnifiedEntity(name="Users"),
            priority=UnifiedEntity(name="2 normal"),
            customer=UnifiedEntity(name="otai@softoft.de")
        ),
    )
    print(f"✓ Created ticket ID: {created_ticket_id}")
    assert int(created_ticket_id) > 0

    print(f"\n=== Retrieving ticket {created_ticket_id}")
    retrieved = await zammad_service.get_ticket(created_ticket_id)
    retrieved_subject = getattr(retrieved, "subject", None) or getattr(retrieved, "title", None) or (
        isinstance(retrieved, dict) and (retrieved.get("subject") or retrieved.get("title"))
    )
    print(f"✓ Retrieved ticket subject: {retrieved_subject}")
    assert retrieved_subject == unique_subject

    print(f"\n=== Searching for tickets (limit=50)")
    hits = await zammad_service.find_tickets(TicketSearchCriteria(limit=50))
    print(f"✓ Found {len(hits)} tickets")

    def _get_id(x: Any) -> str:
        if isinstance(x, dict):
            return str(x.get("id"))
        return str(getattr(x, "id", ""))

    found_in_search = any(_get_id(h) == str(created_ticket_id) for h in hits)
    print(f"✓ Created ticket found in search: {found_in_search}")
    assert found_in_search

    updated_subject = f"{unique_subject} - Updated"
    print(f"\n=== Updating ticket {created_ticket_id} with new subject: {updated_subject}")
    ok = await zammad_service.update_ticket(
        created_ticket_id,
        UnifiedTicket(subject=updated_subject),
    )
    print(f"✓ Update successful: {ok}")
    assert ok is True

    print(f"\n=== Retrieving updated ticket {created_ticket_id}")
    updated = await zammad_service.get_ticket(created_ticket_id)
    updated_title = getattr(updated, "subject", None) or getattr(updated, "title", None) or (
        isinstance(updated, dict) and (updated.get("subject") or updated.get("title"))
    )
    print(f"✓ Updated ticket subject: {updated_title}")
    assert updated_title == updated_subject

    print(f"\n=== Adding note to ticket {created_ticket_id}")
    note_added = await zammad_service.add_note(
        created_ticket_id,
        UnifiedNote(subject="Standalone", body="Standalone note"),
    )
    print(f"✓ Note added: {note_added}")
    assert note_added is True

    print("\n=== Test completed successfully! ===\n")
