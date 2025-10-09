# Ticket System Adapter Architecture

Learn about the ticket system adapter architecture that enables integration with various ticket management systems.

## Adapter Architecture Overview

The adapter pattern provides:
- **Abstraction**: Unified interface for ticket operations
- **Flexibility**: Support multiple ticket systems
- **Extensibility**: Easy to add new adapters
- **Testability**: Mock adapters for testing

## Adapter Interface and Contract

All ticket system adapters must implement the `TicketSystemAdapter` interface:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class TicketSystemAdapter(ABC):
    
    @abstractmethod
    def fetch_tickets(self, criteria: Dict[str, Any]) -> List[Ticket]:
        """Fetch tickets based on search criteria."""
        pass
    
    @abstractmethod
    def update_ticket(self, ticket_id: str, updates: Dict[str, Any]) -> bool:
        """Update ticket properties."""
        pass
    
    @abstractmethod
    def add_note(self, ticket_id: str, note: str, note_type: str) -> bool:
        """Add a note to a ticket."""
        pass
    
    @abstractmethod
    def search_tickets(self, query: str) -> List[Ticket]:
        """Search tickets by query."""
        pass
```

## Fetching and Updating Tickets

### Fetching Tickets

Adapters retrieve tickets based on search criteria:

```python
def fetch_tickets(self, criteria):
    """
    Fetch tickets from the ticket system.
    
    Args:
        criteria: Search criteria dictionary
            - StateType: Ticket state filter
            - QueueIDs: List of queue IDs
            - limit: Maximum number of tickets
            - create_time_after: Minimum creation time
            
    Returns:
        List of Ticket objects
    """
    # Adapter-specific implementation
    pass
```

### Updating Tickets

Adapters update ticket properties:

```python
def update_ticket(self, ticket_id, updates):
    """
    Update ticket properties.
    
    Args:
        ticket_id: Unique ticket identifier
        updates: Dictionary of field updates
            - QueueID: New queue
            - PriorityID: New priority
            - custom_fields: Custom field updates
            
    Returns:
        True if successful, False otherwise
    """
    # Adapter-specific implementation
    pass
```

## Search Criteria and Filtering

### Common Search Fields

- **StateType**: Filter by ticket state (Open, Closed, etc.)
- **QueueIDs**: List of queue IDs to include
- **PriorityID**: Filter by priority
- **create_time_after**: Tickets created after timestamp
- **create_time_before**: Tickets created before timestamp
- **limit**: Maximum number of results

### Advanced Filtering

```python
criteria = {
    "StateType": "Open",
    "QueueIDs": [1, 2, 3],
    "PriorityID": ">3",  # Priority greater than 3
    "create_time_after": "2024-01-01T00:00:00Z",
    "limit": 100,
    "OrderBy": "Created",
    "OrderDirection": "DESC"
}
```

## Error Handling

Adapters should handle common errors:

### Connection Errors

```python
try:
    tickets = adapter.fetch_tickets(criteria)
except ConnectionError as e:
    logger.error(f"Failed to connect: {e}")
    # Retry logic or fallback
```

### Authentication Errors

```python
try:
    adapter.update_ticket(ticket_id, updates)
except AuthenticationError as e:
    logger.error(f"Authentication failed: {e}")
    # Refresh token or alert
```

### Validation Errors

```python
try:
    adapter.update_ticket(ticket_id, {"invalid_field": "value"})
except ValidationError as e:
    logger.error(f"Invalid update: {e}")
    # Handle invalid data
```

### Rate Limiting

```python
try:
    tickets = adapter.fetch_tickets(criteria)
except RateLimitError as e:
    logger.warning(f"Rate limit reached: {e}")
    # Implement backoff strategy
    time.sleep(e.retry_after)
```

## Adapter Lifecycle

1. **Initialization**: Adapter is created with configuration
2. **Connection**: Establish connection to ticket system
3. **Operation**: Perform fetch/update operations
4. **Cleanup**: Close connections, release resources

## Best Practices

### Do:
- Implement all required interface methods
- Handle errors gracefully
- Log operations for debugging
- Respect API rate limits
- Validate input before sending to API
- Use connection pooling for efficiency
- Implement retry logic for transient failures

### Don't:
- Store credentials in code
- Make unbounded requests
- Ignore error responses
- Assume data formats
- Skip input validation
- Create new connections per request

## Testing Adapters

### Unit Tests

Test individual methods:

```python
def test_fetch_tickets():
    adapter = MockTicketAdapter()
    criteria = {"StateType": "Open", "limit": 10}
    tickets = adapter.fetch_tickets(criteria)
    assert len(tickets) <= 10
    assert all(t.state == "Open" for t in tickets)
```

### Integration Tests

Test against real API (test environment):

```python
def test_real_adapter():
    adapter = OtoboAdapter(base_url=TEST_URL, token=TEST_TOKEN)
    criteria = {"limit": 1}
    tickets = adapter.fetch_tickets(criteria)
    assert isinstance(tickets, list)
```

### Contract Tests

Verify adapter implements interface:

```python
def test_adapter_interface():
    adapter = MyCustomAdapter()
    assert isinstance(adapter, TicketSystemAdapter)
    assert hasattr(adapter, 'fetch_tickets')
    assert hasattr(adapter, 'update_ticket')
```

## Related Documentation

- [OTOBO/Znuny Integration](otobo_znuny_integration.md)
- [Custom Adapters](custom_adapters.md)
- [Plugin System](../plugins/plugin_system.md)
