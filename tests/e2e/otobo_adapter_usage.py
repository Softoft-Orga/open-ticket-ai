import asyncio
import logging
import os
import sys


from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedQueue
from open_ticket_ai.base.otobo_integration import OTOBOAdapter
from dotenv import load_dotenv


def create_ticket_system_adapter() -> TicketSystemAdapter:
    load_dotenv()
    base_url = os.environ.get("OTOBO_BASE_URL")
    service = os.environ.get("OTOBO_SERVICE")
    user = os.environ.get("OTOBO_TEST_USER")
    password = os.environ.get("OTOBO_TEST_PASSWORD")
    logger = logging.getLogger(__name__)
    if not all([base_url, service, user, password]):
        logger.error(
            "Please set the OTOBO_BASE_URL, OTOBO_SERVICE, OTOBO_USER, and OTOBO_PASSWORD environment variables."
        )
        sys.exit(1)

    operations: dict[TicketOper, str] = {
        TicketOperation.CREATE: "ticket-create",
        TicketOperation.SEARCH: "ticket-search",
        TicketOperation.GET: "ticket-get",
        TicketOperation.UPDATE: "ticket-update",
        TicketOperation.HISTORY_GET: "ticket-history",
    }

    auth = AuthData(UserLogin=user, Password=password)
    client_config = OTOBOClientConfig(
        base_url=base_url,
        service=service,
        auth=auth,
        operations=operations,
    )
    return OTOBOAdapter(config=None, otobo_client=OTOBOClient(config=client_config))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    adapter = create_ticket_system_adapter()
    print(f"Created adapter: {adapter}")

    tickets = await adapter.find_tickets(criteria=TicketSearchCriteria(queue=UnifiedQueue(name="test")))
    print(f"Found {len(tickets)} tickets")
    print(tickets[0].model_dump())


if __name__ == "__main__":
    asyncio.run(main())
