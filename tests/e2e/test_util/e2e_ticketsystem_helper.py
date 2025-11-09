from typing import Any, Self

from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import TicketCreate, IdName, Article, TicketUpdate, TicketSearch, Ticket

from tests.e2e.test_util.docker_compose_controller import logger
from tests.e2e.test_util.e2e_ticketsystem_config import OtoboE2EConfig


class E2ETicketsystemHelper:
    """Helper class for managing OTOBO tickets during E2E tests"""

    def __init__(self, client: OTOBOZnunyClient, config: OtoboE2EConfig) -> None:
        self._client = client
        self._config = config
        self._created_ticket_ids: list[str] = []

    async def create_ticket(
        self,
        *,
        subject: str,
        body: str,
        queue_name: str | None = None,
    ) -> str:
        """Create a test ticket in OTOBO"""
        env = self._config.environment
        queue_value = queue_name or env.monitored_queue

        logger.info(f"Creating test ticket: subject='{subject}', queue='{queue_value}'")
        ticket = TicketCreate(
            title=subject,
            queue=IdName(name=queue_value),
            state=IdName(name=env.default_state),
            priority=IdName(name=env.default_priority),
            type=IdName(name=env.default_type),
            article=Article(subject=subject, body=body, content_type="text/plain"),
            customer_user=env.default_customer_user,
        )
        created = await self._client.create_ticket(ticket)
        self._created_ticket_ids.append(str(created.id))
        logger.info(f"Ticket created successfully: id={str(created.id)}")
        return str(created.id)

    async def move_ticket_to_queue(self, ticket_id: str, queue_name: str) -> None:
        """Move a ticket to a different queue"""
        logger.debug(f"Moving ticket {ticket_id} to queue '{queue_name}'")
        await self._client.update_ticket(
            TicketUpdate(
                id=int(ticket_id),
                queue=IdName(name=queue_name),
            ),
        )
        logger.debug(f"Ticket {ticket_id} moved to '{queue_name}'")

    async def get_ticket(self, ticket_id: str) -> Ticket:
        """Fetch a ticket by ID"""
        logger.debug(f"Fetching ticket {ticket_id}")
        return await self._client.get_ticket(int(ticket_id))

    async def empty_monitored_queue(self) -> None:
        """Move all tickets from the monitored queue to the cleanup queue"""
        env = self._config.environment
        logger.info(f"Emptying monitored queue: {env.monitored_queue}")

        total_moved = 0

        while ticket_ids := await self._client.search_tickets(
            TicketSearch(queues=[IdName(name=env.monitored_queue)], limit=100)):
            logger.debug(f"Found {len(ticket_ids)} tickets to move")
            for identifier in ticket_ids:
                await self.move_ticket_to_queue(str(identifier), env.cleanup_queue)
                total_moved += 1

        logger.info(f"Monitored queue emptied: {total_moved} tickets moved")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Clean up all tickets created during tests"""
        logger.info(f"Cleaning up {len(self._created_ticket_ids)} test tickets")
        for ticket_id in self._created_ticket_ids:
            await self.move_ticket_to_queue(ticket_id, self._config.environment.cleanup_queue)

        self._created_ticket_ids.clear()
        logger.info("Cleanup complete")
