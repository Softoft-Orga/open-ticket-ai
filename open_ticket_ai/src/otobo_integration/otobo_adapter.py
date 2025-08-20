"""
This module provides an adapter for integrating with the OTOBO ticket system.

The `OTOBOAdapter` class implements the `TicketSystemAdapter` interface to enable
seamless interaction with OTOBO's ticketing API. It handles operations such as:

- Searching for tickets based on custom queries
- Retrieving specific ticket details
- Updating existing ticket records

The adapter uses dependency injection for configuration and client management,
ensuring flexibility and testability.
"""

from injector import inject
from otobo import (
    ArticleDetail, OTOBOClient,
    TicketSearchParams,
    TicketUpdateParams,
)
from otobo.models.ticket_models import TicketCommon

from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote, UnifiedTicket, UnifiedTicketUpdate,
)
from open_ticket_ai.src.otobo_integration.models import TicketAdapter


class OTOBOAdapter(TicketSystemAdapter):
    """Adapter for integrating with the OTOBO ticket system.

    Implements the `TicketSystemAdapter` interface to provide methods for:
    - Searching tickets using custom queries
    - Retrieving ticket details
    - Updating ticket records

    Attributes:
        otobo_client (OTOBOClient): Client instance for interacting with the OTOBO API.
    """

    async def add_note_to_ticket(self, ticket_id: str, note: UnifiedNote) -> bool:
        try:
            update_params: TicketUpdateParams = TicketUpdateParams(
                TicketID=ticket_id,
                Article=ArticleDetail(
                    Subject=note.subject,
                    Body=note.body,
                ),
            )
            await self.otobo_client.update_ticket(payload=update_params)
        except Exception as e:
            print(f"Failed to add note to ticket {ticket_id}: {e}")
            return False
        return True

    @staticmethod
    def get_description() -> str:
        """Return a description of the adapter's functionality.

        Returns:
            str: A description of the OTOBO adapter.
        """
        return "Adapter for OTOBO ticket system integration, providing methods to retrieve and update tickets."

    @inject
    def __init__(self, config: SystemConfig, otobo_client: OTOBOClient):
        """Initialize the OTOBO adapter with configuration and client.

        Args:
            config (SystemConfig): System configuration object containing necessary settings.
            otobo_client (OTOBOClient): Pre-configured client for interacting with the OTOBO API.
        """
        super().__init__(config)
        self.otobo_client = otobo_client

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        """Search for tickets matching the provided criteria.

        Builds a search query from the criteria and uses the OTOBO client
        to retrieve matching tickets. Returns a list of UnifiedTicket objects.

        Currently, the following criteria attributes are supported:
          - id: The ticket ID.
          - subject: The subject of the ticket.

        Args:
            criteria: Search parameters describing the desired tickets.

        Returns:
            list[UnifiedTicket]: A list of matching tickets. Returns an empty list if none are found.

        Example:
            ```python
            criteria = TicketSearchCriteria(subject="Server Issue")
            tickets = await adapter.find_tickets(criteria)
            # Returns list of UnifiedTicket objects. Access attributes like:
            #   tickets[0].id, tickets[0].subject, etc.
            ```
        """
        query: dict = {}
        if criteria.id:
            query["TicketID"] = criteria.id
        if criteria.subject:
            query["Title"] = criteria.subject
        if criteria.queue and criteria.queue.id:
            query["QueueIDs"] = [criteria.queue.id]
        result = await self.otobo_client.search_and_get(query=TicketSearchParams(**query))
        if not result.Ticket:
            return []
        return [TicketAdapter(ticket) for ticket in result.Ticket]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        """Retrieve the first ticket matching the search criteria.

        Uses `find_tickets` to get all matching tickets and returns the first result if available.

        Args:
            criteria: Search parameters formatted as a :class:`TicketSearchCriteria` instance.

        Returns:
            Optional[UnifiedTicket]: The first matching ticket or ``None`` if nothing was found.

        Example:
            ```python
            criteria = TicketSearchCriteria(subject="Server Issue")
            ticket = await adapter.find_first_ticket(criteria)
            if ticket:
                print(f"Found ticket: {ticket.id}")
            ```
        """
        result = await self.find_tickets(criteria)
        return result[0] if len(result) >= 1 else None

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketUpdate) -> bool:
        """Update a ticket record with new data.

        Validates and merges the ticket ID with update data into `TicketUpdateParams`,
        then sends the update request to the OTOBO API.

        Args:
            ticket_id (str): Identifier of the ticket to update.
            updates (UnifiedTicketUpdate): UnifiedTicketUpdate representing fields to update and their new values.

        Returns:
            bool: ``True`` if the update was successful.

        Raises:
            ValidationError: If `updates` contains invalid fields or values for ticket update.

        Example:
            ```python
            success = await adapter.update_ticket("789", {"Priority": "high"})
            # success will be True if the update was successful
            ```
        """
        update_params: TicketUpdateParams = TicketUpdateParams(
            TicketID=ticket_id,
            Ticket=TicketCommon(
                Title=updates.subject,
                QueueID=updates.queue.id if updates.queue and updates.queue.id else None,
                Queue=updates.queue.name if updates.queue and updates.queue.name else None,
                PriorityID=updates.priority.id if updates.priority and updates.priority.id else None,
                Priority=updates.priority.name if updates.priority and updates.priority.name else None,
            ),
        )
        await self.otobo_client.update_ticket(payload=update_params)
        return True

    async def create_ticket(self, ticket_data: UnifiedTicket) -> UnifiedTicket:
        """Create a ticket in OTOBO from a UnifiedTicket instance.

        Converts the provided `UnifiedTicket` into `TicketCreateParams` and sends the creation request
        to the OTOBO API. The returned ticket will have the `id` field updated to the ID assigned by OTOBO.

        Args:
            ticket_data (UnifiedTicket): The ticket data to create.

        Returns:
            UnifiedTicket: The created ticket data with the `id` field updated to the new ticket ID.

        Example:
            ```python
            ticket = UnifiedTicket(subject="New Issue", ...)
            created_ticket = await adapter.create_ticket(ticket)
            print(created_ticket.id)  # Outputs the new ticket ID
            ```
        """
        raise NotImplementedError(
            "Ticket creation is not yet implemented in the OTOBO adapter.",
        )
