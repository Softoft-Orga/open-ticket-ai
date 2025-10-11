# Pipe Factory

The Pipe Factory is responsible for instantiating and registering pipes. It uses the factory pattern to create pipe instances based on configuration.

## Pipe Instantiation Process

1. **Registration**: Pipes are registered with the factory
2. **Configuration**: YAML config specifies which pipes to use
3. **Creation**: Factory creates pipe instances
4. **Injection**: Dependencies are injected into pipes

## Pipe Registration and Discovery

Pipes are registered through:
- Plugin entry points
- Explicit registration in code
- Auto-discovery from modules

## Factory Pattern Implementation

The factory pattern allows:
- Decoupling pipe creation from pipeline logic
- Dynamic pipe selection based on configuration
- Easy testing with mock pipes
- Plugin extensibility

## Custom Pipe Creation

To register a custom pipe, use the `@register_pipe` decorator on your pipe class. This makes the pipe available for use in YAML configuration files.

## Related Documentation

- [Pipes](pipe.md)
- [Plugin Development](../plugins/plugin_development.md)
- [Dependency Injection](dependency_injection.md)
