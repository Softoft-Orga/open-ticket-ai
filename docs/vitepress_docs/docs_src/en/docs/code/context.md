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
- **Read from context**: Use `context.get("key", default_value)` to retrieve data
- **Process data**: Transform or enrich the data as needed
- **Write to context**: Use `context.set("key", value)` to store results
- **Return result**: Return a `PipeResult` indicating success or failure

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

The context provides methods for managing data:
- `get(key, default)`: Retrieve data with an optional default value
- `set(key, value)`: Store data in the context
- `has(key)`: Check if a key exists
- `remove(key)`: Remove a key from the context

## Related Documentation

- [Pipeline System](pipeline.md)
- [Pipes](pipe.md)
- [Services](services.md)
