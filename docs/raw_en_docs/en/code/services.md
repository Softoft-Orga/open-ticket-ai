# Core Services

Services encapsulate business logic and provide reusable functionality to pipes. They are managed by the dependency injection container.

## Core Service Types

### Ticket Services
- **TicketSystemAdapter**: Interface to ticket systems
- **TicketFetcher**: Retrieves tickets
- **TicketUpdater**: Updates ticket properties

### Classification Services
- **ClassificationService**: ML-based classification
- **QueueClassifier**: Queue assignment logic
- **PriorityClassifier**: Priority assignment logic

### Utility Services
- **TemplateRenderer**: Jinja2 template rendering
- **ConfigurationService**: Access to configuration
- **LoggingService**: Centralized logging

## Service Lifecycle Management

Services are typically singletons:
- Created once at application startup
- Shared across all pipes
- Destroyed at application shutdown

## Creating Custom Services

1. Define service interface:

```python
class MyService:
    def do_something(self, data):
        pass
```

2. Implement service:

```python
class MyServiceImpl(MyService):
    def do_something(self, data):
        # Implementation here
        return result
```

3. Register with DI container:

```python
def configure_services(binder):
    binder.bind(MyService, to=MyServiceImpl, scope=singleton)
```

4. Inject into pipes:

```python
from injector import inject

class MyPipe(BasePipe):
    @inject
    def __init__(self, my_service: MyService):
        self.my_service = my_service
```

## Service Best Practices

### Do:
- Keep services focused on single responsibility
- Use interfaces for service contracts
- Make services stateless when possible
- Inject dependencies, don't create them
- Write unit tests for services

### Don't:
- Store execution state in service instances
- Access configuration directly (inject ConfigurationService)
- Create circular dependencies
- Mix business logic with infrastructure concerns

## Testing Services

Services should be unit tested independently:

```python
def test_my_service():
    service = MyServiceImpl()
    result = service.do_something(test_data)
    assert result == expected_result
```

## Related Documentation

- [Dependency Injection](dependency_injection.md)
- [Pipes](pipe.md)
- [Plugin Development](../plugins/plugin_development.md)
