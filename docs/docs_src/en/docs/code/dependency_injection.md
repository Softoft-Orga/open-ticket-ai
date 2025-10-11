# Dependency Injection

Open Ticket AI uses dependency injection (DI) to manage services and their dependencies, promoting loose coupling and testability.

## DI Container Overview

The DI container:
- Manages service lifecycle
- Resolves dependencies automatically
- Supports singleton and transient services
- Enables easy testing with mocks

## Service Registration and Resolution

Services are registered at application startup:

```python
from injector import Injector, singleton

def configure_services(binder):
    binder.bind(TicketService, to=OtoboTicketService, scope=singleton)
    binder.bind(ClassificationService, to=MLClassificationService, scope=singleton)

injector = Injector([configure_services])
```

## UnifiedRegistry Usage

The UnifiedRegistry is the central registry for:
- Services
- Pipes
- Plugins
- Configuration

## Injecting Services into Pipes

Pipes can request services via constructor injection:

```python
from injector import inject

class ClassifyPipe(BasePipe):
    @inject
    def __init__(self, classifier: ClassificationService):
        self.classifier = classifier
    
    def execute(self, context):
        tickets = context.get("tickets")
        results = self.classifier.classify(tickets)
        context.set("results", results)
        return PipeResult.success()
```

## Service Scopes

### Singleton
- One instance for the entire application
- Used for stateless services
- Default scope for most services

### Transient
- New instance for each injection
- Used for stateful services
- Rarely needed in pipe architecture

## Testing with DI

DI makes testing easier:

```python
def test_classify_pipe():
    mock_classifier = Mock(ClassificationService)
    pipe = ClassifyPipe(classifier=mock_classifier)
    
    context = PipelineContext()
    context.set("tickets", [ticket1, ticket2])
    
    result = pipe.execute(context)
    
    assert result.success
    mock_classifier.classify.assert_called_once()
```

## Related Documentation

- [Services](services.md)
- [Pipe Factory](pipe_factory.md)
- [Plugin System](../plugins/plugin_system.md)
