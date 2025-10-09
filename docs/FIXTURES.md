# Test Fixtures Reference

This document catalogs all pytest fixtures available in the Open Ticket AI test suite.

## Fixture Locations

Fixtures are organized hierarchically:

- `tests/conftest.py` - Workspace-level fixtures (available to all tests)
- `tests/unit/conftest.py` - Unit test fixtures
- `tests/unit/core/conftest.py` - Core module fixtures
- `packages/*/tests/conftest.py` - Package-specific fixtures

## Workspace-Level Fixtures (tests/conftest.py)

### Configuration Fixtures

#### `tmp_config(tmp_path: Path) -> Path`
Creates a temporary minimal configuration file for testing.

**Scope:** function  
**Returns:** Path to temporary config.yml  
**Usage:**
```python
def test_config_loading(tmp_config):
    config = load_config(tmp_config)
    assert config.plugins == []
```

#### `test_config(tmp_config: Path) -> RawOpenTicketAIConfig`
Loads and validates test configuration.

**Scope:** function  
**Depends on:** `tmp_config`  
**Returns:** Validated configuration object  
**Usage:**
```python
def test_config_validation(test_config):
    assert isinstance(test_config, RawOpenTicketAIConfig)
    assert test_config.plugins == []
```

#### `app_injector(tmp_config: Path) -> Injector`
Provides a configured dependency injector for testing.

**Scope:** function  
**Depends on:** `tmp_config`  
**Returns:** Configured Injector instance  
**Usage:**
```python
def test_dependency_injection(app_injector):
    config = app_injector.get(RawOpenTicketAIConfig)
    assert config is not None
```

### Pipe Configuration Fixtures

#### `mock_pipe_config() -> dict`
Creates a basic pipe configuration dictionary.

**Scope:** function  
**Returns:** Dictionary with basic pipe config  
**Usage:**
```python
def test_pipe_creation(mock_pipe_config):
    config = mock_pipe_config
    config["id"] = "custom_pipe"
    pipe = MyPipe(config)
```

#### `mock_ticket_system_config() -> dict`
Creates a pipe configuration for ticket system pipes.

**Scope:** function  
**Returns:** Dictionary with ticket_system_id  
**Usage:**
```python
def test_ticket_system_pipe(mock_ticket_system_config):
    pipe = TicketSystemPipe(mock_ticket_system_config)
    assert pipe.ticket_system_id == "mock_ticket_system"
```

## Unit Test Fixtures (tests/unit/conftest.py)

### Context Fixtures

#### `empty_pipeline_context() -> Context`
Provides an empty pipeline context for testing.

**Scope:** function  
**Returns:** Empty Context instance  
**Usage:**
```python
def test_pipe_with_empty_context(empty_pipeline_context):
    result = my_pipe.process(empty_pipeline_context)
    assert result.success
```

### Mock Service Fixtures

#### `mock_ticket_system_service() -> MagicMock`
Provides a mock ticket system service with async methods.

**Scope:** function  
**Returns:** MagicMock configured with AsyncMock methods  
**Mocked Methods:**
- `create_ticket` - returns "TICKET-123"
- `update_ticket` - returns True
- `add_note` - returns True
- `get_ticket` - returns {}

**Usage:**
```python
async def test_ticket_creation(mock_ticket_system_service):
    ticket_id = await mock_ticket_system_service.create_ticket(data)
    assert ticket_id == "TICKET-123"
```

### Configuration Factory Fixtures

#### `pipe_config_factory() -> Callable`
Factory for creating customized pipe configurations.

**Scope:** function  
**Returns:** Factory function that accepts **kwargs  
**Usage:**
```python
def test_custom_pipe_config(pipe_config_factory):
    config = pipe_config_factory(
        id="special_pipe",
        use="SpecialPipe",
        when=False
    )
    assert config["id"] == "special_pipe"
    assert config["when"] is False
```

#### `mock_ticket_system_pipe_config() -> dict`
Configuration dictionary for ticket system pipes.

**Scope:** function  
**Returns:** Dictionary with ticket system pipe config  
**Usage:**
```python
def test_ticket_pipe(mock_ticket_system_pipe_config):
    pipe = MyTicketPipe(mock_ticket_system_pipe_config)
```

### Test Data Fixtures

#### `empty_mocked_ticket_system() -> MockedTicketSystem`
Provides an empty MockedTicketSystem for custom test scenarios.

**Scope:** function  
**Returns:** Empty MockedTicketSystem instance  
**Usage:**
```python
def test_custom_tickets(empty_mocked_ticket_system):
    system = empty_mocked_ticket_system
    system.add_test_ticket(
        id="CUSTOM-1",
        subject="Custom ticket",
        body="Test data"
    )
    tickets = system.get_all_tickets()
    assert len(tickets) == 1
```

#### `mocked_ticket_system() -> MockedTicketSystem`
Provides a MockedTicketSystem pre-populated with test data.

**Scope:** function  
**Returns:** MockedTicketSystem with 3 sample tickets  
**Sample Tickets:**
- TICKET-1: Support queue, Medium priority
- TICKET-2: Development queue, High priority (with note)
- TICKET-3: Support queue, High priority

**Usage:**
```python
def test_ticket_operations(mocked_ticket_system):
    tickets = mocked_ticket_system.get_all_tickets()
    assert len(tickets) == 3
    
    ticket = mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket.subject == "Test ticket 1"
```

### Pipe Runner Fixtures

#### `pipe_runner(mock_registry, mock_ticket_system_service) -> Callable`
Function to run pipes in tests with mocked dependencies.

**Scope:** function  
**Depends on:** `mock_registry` (autouse), `mock_ticket_system_service`  
**Returns:** Function that executes pipes  
**Usage:**
```python
def test_pipe_execution(pipe_runner, pipe_config_factory):
    context = Context()
    config = pipe_config_factory()
    
    result = pipe_runner(MyPipe, config, context)
    assert result.success
```

#### `stateful_pipe_runner(mock_registry, mocked_ticket_system) -> Callable`
Function to run pipes with a stateful mocked ticket system.

**Scope:** function  
**Depends on:** `mock_registry` (autouse), `mocked_ticket_system`  
**Returns:** Function that executes pipes with state  
**Usage:**
```python
def test_stateful_pipe(stateful_pipe_runner, pipe_config_factory):
    context = Context()
    config = pipe_config_factory()
    
    result = stateful_pipe_runner(FetchTicketsPipe, config, context)
    assert len(context.get("tickets")) == 3  # From mocked_ticket_system
```

#### `ticket_system_pipe_factory(mock_ticket_system_service, mock_registry) -> Callable`
Factory for creating ticket system pipes with mocked dependencies.

**Scope:** function  
**Depends on:** `mock_ticket_system_service`, `mock_registry` (autouse)  
**Returns:** Factory function for creating pipes  
**Usage:**
```python
def test_ticket_pipe_creation(ticket_system_pipe_factory):
    pipe = ticket_system_pipe_factory(
        MyTicketPipe,
        ticket_system_id="custom_system"
    )
    assert pipe.ticket_system_id == "custom_system"
```

## Fixture Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `mock_*` | Mock objects/services | `mock_ticket_system_service` |
| `sample_*` | Sample data | `sample_ticket` |
| `tmp_*` | Temporary resources | `tmp_config`, `tmp_path` |
| `empty_*` | Empty/minimal instances | `empty_pipeline_context` |
| `*_factory` | Factory functions | `pipe_config_factory` |

## Using Fixtures

### Basic Usage

```python
def test_with_fixture(fixture_name):
    # fixture_name is automatically injected
    result = do_something(fixture_name)
    assert result
```

### Combining Fixtures

```python
def test_with_multiple_fixtures(
    tmp_config,
    mock_ticket_system_service,
    empty_pipeline_context
):
    # All fixtures are available
    config = load_config(tmp_config)
    # ... test logic
```

### Using Factory Fixtures

```python
def test_with_factory(pipe_config_factory):
    # Call factory to create instances
    config1 = pipe_config_factory(id="pipe1")
    config2 = pipe_config_factory(id="pipe2", when=False)
```

## Discovering Fixtures

List all available fixtures:

```bash
# All fixtures
uv run -m pytest --fixtures

# Fixtures for specific test path
uv run -m pytest tests/unit/ --fixtures

# Search for specific fixture
uv run -m pytest --fixtures | grep mock_
```

Show fixture usage in tests:

```bash
# Find tests using a specific fixture
grep -r "def test_.*mock_ticket_system" tests/
```

## Best Practices

### DO:
- ✅ Use existing fixtures when possible
- ✅ Check `--fixtures` before creating new ones
- ✅ Document new fixtures with docstrings
- ✅ Follow naming conventions
- ✅ Keep fixtures focused and reusable
- ✅ Use factory fixtures for customization

### DON'T:
- ❌ Create duplicate fixtures
- ❌ Make fixtures too complex
- ❌ Use fixtures for setup that belongs in test itself
- ❌ Ignore fixture scope (function/module/session)
- ❌ Create global state in fixtures

## Adding New Fixtures

When adding a new fixture:

1. **Check for existing similar fixtures**
   ```bash
   uv run -m pytest --fixtures | grep -i keyword
   ```

2. **Choose the right location**
   - Workspace-level: Used by all tests
   - Unit-level: Used by unit tests only
   - Package-level: Package-specific only

3. **Follow naming conventions**
   - Use appropriate prefix (`mock_`, `sample_`, `tmp_`, etc.)
   - Use descriptive names

4. **Document the fixture**
   ```python
   @pytest.fixture
   def my_fixture():
       """Clear description of what fixture provides.
       
       Returns: Type and description
       """
       return something
   ```

5. **Update this reference**
   - Add fixture to appropriate section
   - Include usage example

## See Also

- [Testing Guide](../docs/raw_en_docs/en/guides/testing.md)
- [AGENTS.md](../AGENTS.md) - Test structure rules
- [TEST_SETUP_NOTES.md](../TEST_SETUP_NOTES.md) - Historical test setup issues
