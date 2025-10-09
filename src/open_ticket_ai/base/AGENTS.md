# Base Components Guidelines

Guidelines for `src/open_ticket_ai/base/` - reusable pipes and foundational components.

## Purpose of Base

The `base/` module provides abstract base classes and concrete implementations that can be reused across the application and plugins. This is the foundation layer that other modules build upon.

## Base Pipe Classes

When creating or modifying base pipes:

- Define clear abstract interfaces with well-documented contracts
- Use ABC (Abstract Base Class) for interfaces that must be implemented
- Keep base classes focused and cohesive
- Avoid putting business logic in base classes

## Pipe Lifecycle

Base pipes define the lifecycle and execution model:

1. Initialization - constructed by DI container
2. Configuration - validated through pydantic models
3. Execution - `run()` or `execute()` methods called by orchestrator
4. Cleanup - resources released as needed

## Ticket System Pipes

The `ticket_system_pipes/` subdirectory contains reusable pipes for common ticket operations:

- Fetching tickets from systems
- Classifying and analyzing tickets
- Updating ticket properties
- Adding notes and comments

When adding new ticket system pipes:

- Inherit from appropriate base classes
- Make operations idempotent where possible
- Handle partial failures gracefully
- Support batch operations for efficiency

## Mixins and Composition

Use mixins to add orthogonal functionality:

- Keep mixins small and focused on a single concern
- Document mixin requirements clearly
- Use Protocol classes for structural typing where appropriate
- Prefer composition over deep inheritance hierarchies

## Extension Points

Base classes should provide clear extension points:

- Use template method pattern for common workflows
- Allow subclasses to override specific behaviors
- Provide hooks for pre/post processing
- Document which methods are intended for override

## Testing Base Components

Tests for base components should verify:

- Abstract contracts are properly defined
- Base implementations work correctly
- Subclasses can properly extend base behavior
- Mixins compose correctly without conflicts
4