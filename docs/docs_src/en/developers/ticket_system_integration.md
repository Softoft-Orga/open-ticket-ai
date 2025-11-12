# Ticket System Integration

The `TicketSystemService` base class defines a minimal contract for adapters that
integrate external ticketing platforms with Open Ticket AI. The class provides
named coroutine methods that always return `UnifiedTicket` data while accepting
flexible keyword arguments for platform-specific behaviour.

## Flexible Adapter Contracts

Adapters must provide implementations for these methods:

- `find_tickets`
- `find_first_ticket`
- `get_ticket`
- `create_ticket`
- `update_ticket`
- `add_note`

Each method can accept keyword arguments (`**kwargs`) rendered from YAML
configuration. This allows every adapter to expose the argument shapes that the
backing SDK expects without squeezing them into a rigid schema first. Methods
may still accept helper models such as `UnifiedTicket`, but adapters are
responsible for converting their native models back to `UnifiedTicket` before
returning results.

## When to Use Unified Models

Unified models remain available for teams that want a normalized payload. Each
adapter can expose converter helpers (for example
`otai_otobo_znuny.models.otobo_ticket_to_unified_ticket`) to centralize the
translation from native ticket representations into the unified schema. Adapters
can use the same helpers internally, and callers can re-use them when they work
with native models retrieved directly from the upstream SDK.

## YAML Examples

```yaml
services:
  - id: "otobo"
    use: "otobo-znuny:OTOBOZnunyTicketSystemService"
    params:
      webservice_name: "GenericTicketConnector"
      base_url: "https://helpdesk.example.com"
      username: "agent"
      password: "${{ secrets.OTOBO_PASSWORD }}"

pipes:
  - id: "fetch-open"
    use: "otai_base:pipes.ticket_system_pipes.FetchTicketsPipe"
    params:
      ticket_search_criteria:
        queue:
          id: "5"
        limit: 20

  - id: "create"
    use: "my_plugin:CreateTicketPipe"
    params:
      ticket_payload:
        subject: "{{ context.subject }}"
        body: "{{ context.body }}"
```

The YAML snippets above render into keyword arguments that are passed directly
into adapter methods. They can also be converted to unified models in custom
pipes if the workflow expects normalized data.

## Migrating Existing Adapters

1. Remove `@abstractmethod` implementations and enforce only the method names
   defined on `TicketSystemService`.
2. Accept keyword arguments (for example `async def create_ticket(self, **kwargs)`)
   or keep optional unified models if they simplify conversions.
3. Convert native SDK responses into `UnifiedTicket` instances before returning
   from `find_tickets`, `find_first_ticket`, `get_ticket`, and `create_ticket`.
4. Offer helper functions for consumers who need to work with native ticket
   objects directly.

Adapters built with these guidelines will remain compatible with existing
pipelines, while gaining the flexibility to expose richer platform-specific
features.
