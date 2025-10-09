# OTOBO/Znuny Integration Guide

Detailed guide for integrating Open Ticket AI with OTOBO, Znuny, and OTRS ticket systems.

## Overview

Open Ticket AI provides comprehensive integration with:
- **OTOBO** 10.0+
- **Znuny** 6.0+
- **OTRS** 6.0+ (limited support)

## API Authentication

### API Token Authentication (Recommended)

Most secure method using API tokens:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"
      verify_ssl: true
```

**Setting up API token:**
1. Log in to OTOBO/Znuny as admin
2. Navigate to Admin → API Token Management
3. Create new token with required permissions
4. Copy token and set as environment variable

### Session-based Authentication

For systems without API token support:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      username: "${OTOBO_USERNAME}"
      password: "${OTOBO_PASSWORD}"
```

**Security Note**: API tokens are preferred as they:
- Can be easily revoked
- Don't expose user passwords
- Support granular permissions
- Can be rotated regularly

## Ticket Operations

### Fetching Tickets

Retrieve tickets based on criteria:

```yaml
pipes:
  - pipe_name: fetch_tickets
    search:
      StateType: "Open"
      QueueIDs: [1, 2, 3]
      limit: 100
      create_time_after: "{{ now() - timedelta(hours=24) }}"
```

**Common Search Parameters:**
- `StateType`: "Open", "Closed", "New", etc.
- `QueueIDs`: List of queue IDs
- `PriorityID`: Priority level (1-5 or custom)
- `CustomerUserLogin`: Filter by customer
- `limit`: Maximum results

### Updating Tickets

Update ticket properties:

```yaml
pipes:
  - pipe_name: update_ticket
    ticket_id: "{{ context.ticket.id }}"
    updates:
      QueueID: "{{ context.predicted_queue_id }}"
      PriorityID: "{{ context.predicted_priority_id }}"
      StateID: 2  # Set to specific state
```

**Updatable Fields:**
- `QueueID`: Move to different queue
- `PriorityID`: Change priority
- `StateID`: Update ticket state
- `OwnerID`: Assign to agent
- `Title`: Update ticket title

### Adding Notes/Articles

Add notes or articles to tickets:

```yaml
pipes:
  - pipe_name: add_note
    ticket_id: "{{ context.ticket.id }}"
    note_text: "Automatically classified by AI"
    note_type: "internal"  # or "external"
    content_type: "text/plain"
```

**Note Types:**
- `internal`: Only visible to agents
- `external`: Visible to customer

## Custom Field Handling

### Reading Custom Fields

Access dynamic fields (custom fields):

```yaml
pipes:
  - pipe_name: read_custom_field
    ticket_id: "{{ context.ticket.id }}"
    field_name: "CustomerCategory"
    store_in_context: "customer_category"
```

### Updating Custom Fields

Update dynamic field values:

```yaml
pipes:
  - pipe_name: update_custom_field
    ticket_id: "{{ context.ticket.id }}"
    field_name: "AIConfidence"
    field_value: "{{ context.confidence * 100 }}"
```

**Supported Field Types:**
- Text
- Dropdown
- Multiselect
- Date
- DateTime
- Integer

### Custom Field Configuration

```yaml
plugins:
  - name: otobo_znuny
    config:
      custom_fields:
        AIClassification:
          type: "Text"
        AIConfidence:
          type: "Integer"
```

## Known Limitations

### Version Differences

**OTOBO 10.0+**
- Full REST API support
- All features supported
- Recommended version

**Znuny 6.0+**
- Good REST API support
- Most features work
- Minor API differences

**OTRS 6.0+**
- Limited REST API
- Basic operations only
- Consider upgrading to OTOBO/Znuny

### API Limitations

- **Rate Limiting**: Default 100 requests/minute
- **Batch Size**: Maximum 100 tickets per request
- **Custom Fields**: Not all field types supported
- **Attachments**: Limited to certain operations

### Performance Considerations

- Large result sets can be slow
- Custom field queries add overhead
- Complex searches impact performance
- Consider pagination for large datasets

## Configuration Examples

### Basic Setup

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "https://tickets.example.com"
      api_token: "${OTOBO_API_TOKEN}"

orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search:
            StateType: "Open"
            limit: 50
        - pipe_name: classify_queue
        - pipe_name: update_ticket
```

### Advanced Setup

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"
      verify_ssl: true
      timeout: 60
      max_retries: 3
      retry_delay: 5

orchestrator:
  pipelines:
    - name: full_classification
      run_every_milli_seconds: 300000
      pipes:
        - pipe_name: fetch_tickets
          search:
            StateType: "Open"
            QueueIDs: [1, 2, 3, 4, 5]
            limit: 100
        - pipe_name: classify_queue
          confidence_threshold: 0.7
        - pipe_name: classify_priority
          confidence_threshold: 0.8
        - pipe_name: update_ticket
        - pipe_name: add_note
          note_text: "Auto-classified: Q={{ context.queue }}, P={{ context.priority }}"
          note_type: "internal"
```

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to OTOBO/Znuny
**Solutions**:
- Verify base URL is correct
- Check network connectivity
- Verify SSL certificates (or disable verify_ssl for testing)
- Check firewall rules

### Authentication Failures

**Problem**: 401 Unauthorized errors
**Solutions**:
- Verify API token is valid
- Check token hasn't expired
- Ensure user has required permissions
- Try regenerating token

### Ticket Updates Fail

**Problem**: Updates don't apply or return errors
**Solutions**:
- Verify ticket exists
- Check user has update permissions
- Validate field values (queue IDs, priority IDs)
- Review error messages in logs

### Performance Issues

**Problem**: Slow ticket fetching
**Solutions**:
- Reduce limit parameter
- Use more specific search criteria
- Avoid complex custom field queries
- Implement pagination
- Check OTOBO/Znuny server performance

## Related Documentation

- [Ticket Systems Architecture](ticket_systems.md)
- [OTOBO/Znuny Plugin](../plugins/otobo_znuny.md)
- [Configuration Examples](../configuration/examples.md)
