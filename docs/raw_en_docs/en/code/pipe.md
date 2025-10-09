# Pipes

Pipes are the individual processing components in a pipeline. Each pipe performs a specific task and follows a consistent interface for input/output handling.

## What is a Pipe?

A pipe is a stateless component that:
- Receives input data
- Performs a specific operation
- Returns a result
- Can access shared services via dependency injection

## Pipe Interface and Contract

All pipes must implement the base pipe interface:

```python
class BasePipe:
    def execute(self, context: PipelineContext) -> PipeResult:
        """Execute the pipe's logic."""
        pass
```

## Input/Output Handling

Pipes interact with the execution context:
- **Input**: Read data from context
- **Processing**: Transform or enrich data
- **Output**: Write results back to context

## Stateless Execution Model

Pipes are designed to be stateless:
- No instance variables should store execution state
- All data flows through the context
- Each execution is independent

## Built-in Pipe Types

Open Ticket AI includes several built-in pipes:

### Data Fetching
- `FetchTicketsPipe`: Retrieve tickets from ticket system
- `SearchTicketsPipe`: Search for specific tickets

### Processing
- `ClassifyQueuePipe`: Classify tickets into queues
- `ClassifyPriorityPipe`: Assign priority levels
- `EnrichTicketPipe`: Add additional data to tickets

### Output
- `UpdateTicketPipe`: Update ticket properties
- `AddNotePipe`: Add notes to tickets
- `SendNotificationPipe`: Send notifications

## Custom Pipes

See [Creating Custom Pipes](../plugins/plugin_development.md) for information on building your own pipes.

## Related Documentation

- [Pipeline System](pipeline.md)
- [Pipe Factory](pipe_factory.md)
- [Context](context.md)
- [Plugin Development](../plugins/plugin_development.md)
