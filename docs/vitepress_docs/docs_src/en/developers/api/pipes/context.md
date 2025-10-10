# Pipeline Execution Context

The execution context is a shared data structure that flows through the pipeline, allowing pipes to share data and maintain state during execution.

## Execution Context Concept

The context object:
- Stores intermediate results
- Shares data between pipes
- Maintains execution metadata
- Provides access to services

## Sharing Data Between Pipes

Pipes can read and write to the context:

```python
def execute(self, context):
    # Read from context
    tickets = context.get("tickets", [])
    
    # Process data
    classified = self.classify(tickets)
    
    # Write to context
    context.set("classified_tickets", classified)
    
    return PipeResult.success()
```

## Context Lifecycle

1. **Created**: Context is created before pipeline execution
2. **Populated**: Initial data is added to context
3. **Shared**: Pipes read and write during execution
4. **Cleaned**: Context is cleared after execution

## Best Practices for Context Usage

### Do:
- Use descriptive keys for context data
- Document what data your pipe expects
- Clean up temporary data
- Use type hints for context data

### Don't:
- Store large objects unnecessarily
- Modify context data in-place without documenting
- Rely on undocumented context keys
- Use context for pipe configuration (use DI instead)

## Context API

```python
# Get data with default
value = context.get("key", default_value)

# Set data
context.set("key", value)

# Check if key exists
if context.has("key"):
    # ...

# Remove key
context.remove("key")
```

## Related Documentation

- [Pipeline System](pipeline.md)
- [Pipes](pipe.md)
- [Services](services.md)
