---
description: Discover our Python library for seamless ticket system integration. This
  documentation details the `TicketSystemAdapter`, an abstract base class for building
  custom connectors, and provides a ready-to-use `OTOBOAdapter`. Learn to manage tickets
  across different platforms using unified models like `UnifiedTicket`, `UnifiedNote`,
  and `TicketSearchCriteria` for creating, updating, and finding support tickets.
---
# Documentation for `**/ce/ticket_system_integration/*.py`

## Module: `open_ticket_ai\src\ce\ticket_system_integration\otobo_adapter.py`

Package for integrating with OTOBO systems.
This module provides the primary interface for OTOBO integration by exposing
the `OTOBOAdapter` class. It serves as the public API entry point for
interacting with OTOBO services.



---

## Module: `open_ticket_ai\src\ce\ticket_system_integration\otobo_adapter_config.py`



---

## Module: `open_ticket_ai\src\ce\ticket_system_integration\ticket_system_adapter.py`


### <span style='text-info'>class</span> `TicketSystemAdapter`

An abstract base class for ticket system adapters.
This class defines the interface that all concrete ticket system adapters must
implement to interact with different ticketing systems. It provides common
configuration handling through dependency injection and requires subclasses
to implement core ticket operations.

**Parameters:**

- **`config`** (`SystemConfig`) - System configuration object containing adapter settings.


::: details #### <Badge type="info" text="method"/> <span class='text-warning'>def</span> `__init__(self, config: SystemConfig)`
Initialize the adapter with system configuration.
This constructor is automatically injected with the system configuration
using the dependency injection framework. It initializes the adapter
with the provided configuration and ensures proper setup of inherited
components.

**Parameters:**

- **`config`** (`SystemConfig`) - The system configuration object containing
all necessary settings and parameters for the adapter.

:::


::: details #### <Badge type="info" text="method"/> <span class="text-warning">async def</span> `update_ticket(self, ticket_id: str, updates: dict) -> bool`
Update a ticket in the system.
This method must be implemented by concrete adapters to handle updating
ticket attributes in the target ticketing system. It should support partial
updates and return the updated ticket representation.

**Parameters:**

- **`ticket_id`** () - Unique identifier of the ticket to update.
- **`updates`** () - Dictionary of attributes to update on the ticket.

**Returns:** (`bool`) - ``True`` if the update succeeded, otherwise ``False``.

:::


::: details #### <Badge type="info" text="method"/> <span class="text-warning">async def</span> `find_tickets(self, criteria: SearchCriteria) -> list[UnifiedTicket]`
Search for tickets matching ``criteria``.
This method must be implemented by concrete adapters to perform
complex searches against the target ticketing system. The query
structure is adapter-specific but should support common filtering
and search operations.

**Parameters:**

- **`criteria`** () - Parameters defining which tickets to search for.

**Returns:** (`list[UnifiedTicket]`) - A list of tickets that match the criteria.
Returns an empty list if no matches are found.

:::


::: details #### <Badge type="info" text="method"/> <span class="text-warning">async def</span> `find_first_ticket(self, criteria: SearchCriteria) -> UnifiedTicket | None`
Return the first ticket that matches ``criteria`` if any.
This is a convenience method that should return the first matching
ticket from a search operation. It should optimize for performance
by limiting results internally.

**Parameters:**

- **`criteria`** () - Parameters defining which ticket to search for.

**Returns:** (`Optional[UnifiedTicket]`) - The first matching ticket or ``None`` if no tickets match.

:::


::: details #### <Badge type="info" text="method"/> <span class="text-warning">async def</span> `create_ticket(self, ticket_data: UnifiedTicket) -> UnifiedTicket`
Create a new ticket in the system.
This method must be implemented by concrete adapters to handle ticket creation
in the target ticketing system. The ticket data is provided in a unified format.

**Parameters:**

- **`ticket_data`** (`UnifiedTicket`) - The ticket data to create. Contains all necessary fields in a
system-agnostic format.

**Returns:** (`UnifiedTicket`) - The created ticket object with system-generated identifiers and fields.

:::


::: details #### <Badge type="info" text="method"/> <span class="text-warning">async def</span> `add_note(self, ticket_id: str, note: UnifiedNote) -> UnifiedNote`
Add a note to an existing ticket.
This method must be implemented by concrete adapters to attach notes/comments
to tickets in the target system. The note content is provided in a unified format.

**Parameters:**

- **`ticket_id`** (`str`) - Unique identifier of the target ticket.
- **`note`** (`UnifiedNote`) - The note content and metadata to add.

**Returns:** (`UnifiedNote`) - The added note object with system-generated metadata (e.g., timestamp, ID).

:::


---

## Module: `open_ticket_ai\src\ce\ticket_system_integration\unified_models.py`


### <span style='text-info'>class</span> `UnifiedEntity`

Base entity with optional ID and name.

**Parameters:**

- **`id`** (`Optional[int]`) (default: `None`) - Unique identifier for the entity. Defaults to None.
- **`name`** (`Optional[str]`) (default: `None`) - Display name of the entity. Defaults to None.

### <span style='text-info'>class</span> `UnifiedUser`

Represents a user within the system.
Inherits attributes from `UnifiedEntity` and adds:

**Parameters:**

- **`email`** (`Optional[str]`) (default: `None`) - Email address of the user. Defaults to None.

### <span style='text-info'>class</span> `UnifiedQueue`

Represents a ticket queue.
Inherits attributes from `UnifiedEntity`.

### <span style='text-info'>class</span> `UnifiedPriority`

Represents a ticket priority level.
Inherits attributes from `UnifiedEntity`.

### <span style='text-info'>class</span> `UnifiedStatus`

Represents a ticket status.
Inherits attributes from `UnifiedEntity`.

### <span style='text-info'>class</span> `UnifiedNote`

Represents a note attached to a ticket.

**Parameters:**

- **`id`** (`Optional[str]`) (default: `None`) - Unique identifier for the note. Defaults to None.
- **`body`** (`str`) - Content of the note.
- **`created_at`** (`datetime`) - Timestamp when the note was created.
- **`is_internal`** (`bool`) - Indicates if the note is internal (not visible to customers).
- **`author`** (`UnifiedUser`) - User who created the note.

### <span style='text-info'>class</span> `UnifiedTicket`

Unified representation of a support ticket.

**Parameters:**

- **`id`** (`str`) - Unique identifier for the ticket.
- **`subject`** (`str`) - Subject line of the ticket.
- **`body`** (`str`) - Main content/description of the ticket.
- **`custom_fields`** (`Dict`) - Additional custom field data associated with the ticket.
- **`queue`** (`UnifiedQueue`) - Queue to which the ticket belongs.
- **`priority`** (`UnifiedPriority`) - Priority level of the ticket.
- **`status`** (`UnifiedStatus`) - Current status of the ticket.
- **`owner`** (`UnifiedUser`) - User currently assigned to the ticket.
- **`notes`** (`List[UnifiedNote]`) (default: `empty list`) - List of notes attached to the ticket. Defaults to empty list.

### <span style='text-info'>class</span> `SearchCriteria`

Criteria for searching/filtering tickets.

**Parameters:**

- **`id`** (`Optional[str]`) (default: `None`) - Ticket ID to search for. Defaults to None.
- **`subject`** (`Optional[str]`) (default: `None`) - Text to search in ticket subjects. Defaults to None.
- **`queue`** (`Optional[UnifiedQueue]`) (default: `None`) - Queue to filter by. Defaults to None.
- **`user`** (`Optional[UnifiedUser]`) (default: `None`) - User to filter by (e.g., owner). Defaults to None.


---
