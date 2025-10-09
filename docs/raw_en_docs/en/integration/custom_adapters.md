# Building Custom Ticket System Adapters

Guide for creating custom adapters to integrate Open Ticket AI with other ticket management systems.

## Why Create a Custom Adapter?

Custom adapters enable integration with:
- Proprietary ticket systems
- Legacy systems
- Custom-built ticketing platforms
- Systems without built-in adapters

## Implementing the Adapter Interface

### 1. Create Adapter Class

Implement the `TicketSystemAdapter` interface:

```python
from open_ticket_ai.integration import TicketSystemAdapter
from typing import List, Dict, Any

class MyCustomAdapter(TicketSystemAdapter):
    """Adapter for My Custom Ticket System."""
    
    def __init__(self, base_url: str, api_key: str, **kwargs):
        """Initialize adapter with configuration."""
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = kwargs.get('timeout', 30)
        self.session = self._create_session()
    
    def _create_session(self):
        """Create HTTP session with authentication."""
        import requests
        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        return session
```

### 2. Implement Required Methods

#### fetch_tickets

```python
def fetch_tickets(self, criteria: Dict[str, Any]) -> List[Ticket]:
    """
    Fetch tickets based on search criteria.
    
    Args:
        criteria: Search parameters
            - state: Ticket state filter
            - queue_ids: List of queue IDs
            - limit: Maximum results
            
    Returns:
        List of Ticket objects
    """
    # Build API request
    params = self._build_search_params(criteria)
    
    # Make API call
    response = self.session.get(
        f"{self.base_url}/api/tickets",
        params=params,
        timeout=self.timeout
    )
    response.raise_for_status()
    
    # Parse response
    data = response.json()
    tickets = [self._parse_ticket(t) for t in data['tickets']]
    
    return tickets
```

#### update_ticket

```python
def update_ticket(self, ticket_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update ticket properties.
    
    Args:
        ticket_id: Ticket identifier
        updates: Field updates
        
    Returns:
        True if successful
    """
    # Build update payload
    payload = self._build_update_payload(updates)
    
    # Make API call
    response = self.session.put(
        f"{self.base_url}/api/tickets/{ticket_id}",
        json=payload,
        timeout=self.timeout
    )
    
    return response.status_code == 200
```

#### add_note

```python
def add_note(self, ticket_id: str, note: str, note_type: str = "internal") -> bool:
    """
    Add note to ticket.
    
    Args:
        ticket_id: Ticket identifier
        note: Note content
        note_type: "internal" or "public"
        
    Returns:
        True if successful
    """
    payload = {
        'content': note,
        'type': note_type,
        'timestamp': datetime.now().isoformat()
    }
    
    response = self.session.post(
        f"{self.base_url}/api/tickets/{ticket_id}/notes",
        json=payload,
        timeout=self.timeout
    )
    
    return response.status_code == 201
```

#### search_tickets

```python
def search_tickets(self, query: str) -> List[Ticket]:
    """
    Search tickets by query string.
    
    Args:
        query: Search query
        
    Returns:
        List of matching tickets
    """
    response = self.session.get(
        f"{self.base_url}/api/tickets/search",
        params={'q': query},
        timeout=self.timeout
    )
    response.raise_for_status()
    
    data = response.json()
    return [self._parse_ticket(t) for t in data['results']]
```

### 3. Helper Methods

```python
def _build_search_params(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Convert generic criteria to system-specific parameters."""
    params = {}
    
    if 'StateType' in criteria:
        params['state'] = criteria['StateType']
    
    if 'QueueIDs' in criteria:
        params['queue_ids'] = ','.join(map(str, criteria['QueueIDs']))
    
    if 'limit' in criteria:
        params['limit'] = criteria['limit']
    
    return params

def _parse_ticket(self, raw_ticket: Dict) -> Ticket:
    """Parse system-specific ticket format to Ticket object."""
    return Ticket(
        id=raw_ticket['id'],
        title=raw_ticket['subject'],
        description=raw_ticket['body'],
        state=raw_ticket['status'],
        priority=raw_ticket['priority_level'],
        queue_id=raw_ticket['department_id'],
        created_at=raw_ticket['created'],
        updated_at=raw_ticket['modified']
    )
```

## Testing Custom Adapters

### Unit Tests

Test individual methods in isolation:

```python
import pytest
from unittest.mock import Mock, patch

def test_fetch_tickets():
    # Mock HTTP response
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'tickets': [
                {'id': '1', 'subject': 'Test', 'status': 'open'}
            ]
        }
        
        adapter = MyCustomAdapter(
            base_url='https://api.example.com',
            api_key='test-key'
        )
        
        tickets = adapter.fetch_tickets({'StateType': 'Open'})
        
        assert len(tickets) == 1
        assert tickets[0].id == '1'
        assert tickets[0].title == 'Test'
```

### Integration Tests

Test against real API (test environment):

```python
def test_adapter_integration():
    adapter = MyCustomAdapter(
        base_url=TEST_BASE_URL,
        api_key=TEST_API_KEY
    )
    
    # Test fetch
    tickets = adapter.fetch_tickets({'limit': 1})
    assert len(tickets) >= 0
    
    # Test update (if tickets exist)
    if tickets:
        success = adapter.update_ticket(
            tickets[0].id,
            {'priority': 'high'}
        )
        assert success
```

### Contract Tests

Verify adapter implements interface correctly:

```python
def test_adapter_interface():
    adapter = MyCustomAdapter(
        base_url='https://api.example.com',
        api_key='test-key'
    )
    
    # Verify instance
    assert isinstance(adapter, TicketSystemAdapter)
    
    # Verify methods exist
    assert callable(adapter.fetch_tickets)
    assert callable(adapter.update_ticket)
    assert callable(adapter.add_note)
    assert callable(adapter.search_tickets)
```

## Packaging and Distribution

### 1. Create Plugin Structure

```
my-ticket-adapter/
├── pyproject.toml
├── README.md
├── src/
│   └── my_ticket_adapter/
│       ├── __init__.py
│       ├── adapter.py
│       └── plugin.py
└── tests/
    └── test_adapter.py
```

### 2. Plugin Configuration

```toml
# pyproject.toml
[project]
name = "my-ticket-adapter"
version = "1.0.0"
dependencies = [
    "open-ticket-ai>=1.0.0",
    "requests>=2.31.0"
]

[project.entry-points."open_ticket_ai.plugins"]
my_ticket_adapter = "my_ticket_adapter.plugin:setup"
```

### 3. Plugin Setup

```python
# plugin.py
from my_ticket_adapter.adapter import MyCustomAdapter

def setup(registry):
    """Register adapter with Open Ticket AI."""
    registry.register_adapter("my_custom", MyCustomAdapter)
```

### 4. Build and Publish

```bash
# Build
uv build

# Publish to PyPI
uv publish

# Or install locally for testing
uv pip install -e .
```

## Best Practices

### Error Handling

```python
def fetch_tickets(self, criteria):
    try:
        response = self.session.get(url, params=params)
        response.raise_for_status()
    except requests.ConnectionError:
        raise ConnectionError("Failed to connect to ticket system")
    except requests.Timeout:
        raise TimeoutError("Request timed out")
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            raise AuthenticationError("Invalid credentials")
        elif e.response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        raise
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=10)
)
def fetch_tickets(self, criteria):
    # Implementation with automatic retries
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def update_ticket(self, ticket_id, updates):
    logger.debug(f"Updating ticket {ticket_id} with {updates}")
    
    try:
        response = self.session.put(url, json=payload)
        response.raise_for_status()
        logger.info(f"Successfully updated ticket {ticket_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to update ticket {ticket_id}: {e}")
        raise
```

## Related Documentation

- [Ticket System Architecture](ticket_systems.md)
- [Plugin Development](../plugins/plugin_development.md)
- [API Compatibility](api_compatibility.md)
