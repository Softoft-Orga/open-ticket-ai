# OTOBO/Znuny Plugin

The OTOBO/Znuny plugin provides integration with OTOBO, Znuny, and OTRS ticket systems.

## Overview

This plugin implements:
- Ticket system adapter for OTOBO/Znuny/OTRS
- Ticket fetching and updating
- Custom field support
- Authentication handling

## Ticket System Adapter Implementation

The plugin provides a complete `TicketSystemAdapter` implementation that:
- Connects to OTOBO/Znuny REST API
- Fetches tickets based on search criteria
- Updates ticket properties
- Manages custom fields

## Authentication and Connection

### API Token Authentication

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "https://your-otobo-instance.com"
      api_token: "${OTOBO_API_TOKEN}"
      verify_ssl: true
```

### Session-based Authentication

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "https://your-otobo-instance.com"
      username: "${OTOBO_USERNAME}"
      password: "${OTOBO_PASSWORD}"
```

## Supported Operations

### Fetch Tickets

```yaml
pipes:
  - pipe_name: fetch_tickets
    search_criteria:
      StateType: "Open"
      QueueIDs: [1, 2, 3]
      limit: 100
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

## Custom Field Handling

### Reading Custom Fields

```yaml
pipes:
  - pipe_name: read_custom_field
    field_name: "CustomerCategory"
```

### Updating Custom Fields

```yaml
pipes:
  - pipe_name: update_custom_field
    field_name: "AIClassification"
    field_value: "{{ context.classification_result }}"
```

## Known Limitations

### API Rate Limits
- Respect API rate limits
- Implement backoff strategies
- Use batch operations when possible

### Version Compatibility
- OTOBO 10.0+
- Znuny 6.0+
- OTRS 6.0+ (limited support)

### Custom Field Types
- Not all custom field types supported
- Test with your schema
- Check field type compatibility

## Configuration Reference

### Required Settings
- `base_url`: OTOBO/Znuny instance URL
- Authentication credentials (token or username/password)

### Optional Settings
- `verify_ssl`: SSL certificate verification (default: true)
- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Maximum retry attempts (default: 3)
- `retry_delay`: Delay between retries in seconds (default: 5)

## Troubleshooting

### Connection Issues
- Verify base URL is correct
- Check network connectivity
- Verify SSL certificates
- Check firewall rules

### Authentication Failures
- Verify credentials are correct
- Check token expiration
- Verify user permissions
- Check authentication method

### Update Failures
- Verify ticket exists
- Check user permissions
- Validate field values
- Review error logs

## Related Documentation

- [OTOBO/Znuny Integration](../integration/otobo_znuny_integration.md)
- [Ticket Systems](../integration/ticket_systems.md)
- [Configuration Examples](../details/configuration/examples.md)
