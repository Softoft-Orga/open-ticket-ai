---
description: OTOBO, Znuny, and OTRS plugin for Open Ticket AI providing ticket system integration with fetching, updating, and username/password authentication.
---

# OTOBO/Znuny Plugin

The OTOBO/Znuny plugin provides integration with OTOBO, Znuny, and OTRS ticket systems.

## Overview

This plugin implements:

- Ticket system adapter for OTOBO/Znuny/OTRS
- Ticket fetching and updating
- Username/password authentication
- Queue-based ticket search

## Ticket System Adapter Implementation

The plugin provides a complete `TicketSystemAdapter` implementation that:

- Connects to OTOBO/Znuny REST API
- Fetches tickets based on queue criteria
- Updates ticket properties
- Manages authentication sessions

## Authentication and Connection

The plugin uses **username and password authentication** only. Configure your credentials:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "https://your-otobo-instance.com"
      username: "${OTOBO_USERNAME}"
      password: "${OTOBO_PASSWORD}"
      verify_ssl: true
```

**Important**: API token authentication is not supported. You must use username and password credentials.

## Supported Operations

### Fetch Tickets

The plugin supports queue-based ticket search with pagination:

```yaml
pipes:
  - pipe_name: fetch_tickets
    search_criteria:
      queue:
        id: "1"
        name: "Support"
      limit: 50
      offset: 0
```

**Search Criteria Fields:**

- `queue`: (Optional) UnifiedEntity with `id` and/or `name` to filter by queue
- `limit`: (Optional) Maximum number of tickets to fetch (default: 10)
- `offset`: (Optional) Number of tickets to skip for pagination (default: 0)

**Example - Fetch by Queue Name:**

```yaml
pipes:
  - pipe_name: fetch_tickets
    search_criteria:
      queue:
        name: "Support"
      limit: 100
```

**Example - Fetch All (No Queue Filter):**

```yaml
pipes:
  - pipe_name: fetch_tickets
    search_criteria:
      limit: 50
      offset: 0
```

**Example - Pagination:**

```yaml
pipes:
  - pipe_name: fetch_tickets_page_1
    search_criteria:
      queue:
        name: "Billing"
      limit: 25
      offset: 0

  - pipe_name: fetch_tickets_page_2
    search_criteria:
      queue:
        name: "Billing"
      limit: 25
      offset: 25
```

### Update Tickets

```yaml
pipes:
  - pipe_name: update_ticket
    updates:
      QueueID: "{{ context.predicted_queue_id }}"
      PriorityID: "{{ context.predicted_priority_id }}"
```

### Add Notes

```yaml
pipes:
  - pipe_name: add_note
    note_text: "Automatically classified by AI"
    note_type: "internal"
```

## Known Limitations

### Search Functionality

- **Only queue-based search is supported**
- No support for StateType, TicketNumber, or other advanced filters
- Cannot search by priority, state, or custom fields
- Use queue filtering and post-process results if needed

### Authentication

- **No API token support** - only username/password authentication
- Session management handled automatically by the plugin
- Credentials must have appropriate permissions

### API Rate Limits

- Respect API rate limits
- Implement backoff strategies
- Use pagination for large result sets

### Version Compatibility

- OTOBO 10.0+
- Znuny 6.0+
- OTRS 6.0+ (limited support)

## Configuration Reference

### Required Settings

- `base_url`: OTOBO/Znuny instance URL
- `username`: Username for authentication
- `password`: Password for authentication

### Optional Settings

- `verify_ssl`: SSL certificate verification (default: true)
- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Maximum retry attempts (default: 3)
- `retry_delay`: Delay between retries in seconds (default: 5)

## Troubleshooting

### Connection Issues

- Verify base URL is correct and accessible
- Check network connectivity
- Verify SSL certificates (or temporarily disable with `verify_ssl: false` for testing)
- Check firewall rules allow outbound connections

### Authentication Failures

- Verify username and password are correct
- Check user account is active and not locked
- Verify user has appropriate permissions
- Ensure credentials are properly set in environment variables

### No Tickets Returned

- Verify queue name or ID is correct
- Check user has permission to access the specified queue
- Try fetching without queue filter to verify connection works
- Verify tickets exist in the specified queue

### Update Failures

- Verify ticket exists and user has write permissions
- Check that QueueID and PriorityID values are valid
- Validate field values match OTOBO/Znuny requirements
- Review error logs for specific error messages

## Workarounds for Search Limitations

Since only queue-based search is supported, you can work around limitations by:

**1. Fetch and Filter in Pipeline:**

```yaml
pipes:
  - pipe_name: fetch_all_tickets
    search_criteria:
      limit: 100
  
  - pipe_name: filter_open_tickets
    # Use custom pipe to filter by state
    filter_condition: "{{ ticket.state == 'Open' }}"
```

**2. Fetch Multiple Queues:**

```yaml
pipes:
  - pipe_name: fetch_support_queue
    search_criteria:
      queue:
        name: "Support"
      limit: 50
  
  - pipe_name: fetch_billing_queue
    search_criteria:
      queue:
        name: "Billing"
      limit: 50
```

**3. Use Pagination for Large Datasets:**

```yaml
pipes:
  - pipe_name: fetch_page_1
    search_criteria:
      queue:
        name: "Support"
      limit: 50
      offset: 0
  
  - pipe_name: fetch_page_2
    search_criteria:
      queue:
        name: "Support"
      limit: 50
      offset: 50
```

## Related Documentation

- [Ticket System Integration](../concepts/ticket_system_integration.md)
- [First Pipeline Tutorial](../guides/first_pipeline.md)
- [Configuration Examples](../details/config_reference.md)
