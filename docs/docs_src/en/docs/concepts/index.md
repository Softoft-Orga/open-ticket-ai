# Core Concepts

This directory contains architectural documentation that explains the fundamental concepts and design of Open Ticket AI.

## What's in Concepts?

The concepts documentation focuses on **what** the system is and **why** it's designed that way, rather than **how** to use it.

### Available Documentation

- **[Pipeline System](pipeline.md)** - Comprehensive guide to pipelines with diagrams explaining:
  - What pipelines are and how they work
  - Pipeline orchestration lifecycle (rendering and execution)
  - When and how pipelines are triggered and executed
  - Relationship between pipes, composite pipes, and steps
  - PlantUML architecture and sequence diagrams
  - Implementation references and best practices

- **[Pipeline Architecture](pipeline-architecture.md)** - Complete overview of the pipeline system including:
  - Pipeline execution model and lifecycle
  - Pipe system and interface
  - Orchestrator scheduling and supervision
  - Execution context and data sharing
  - Pipe factory pattern and registration
  - Best practices for pipeline design

- **[Configuration and Template Rendering](config_rendering.md)** - Visual guide to configuration loading and rendering:
  - Configuration lifecycle from YAML to runtime objects
  - Template rendering architecture and process flow
  - Environment variable substitution
  - Jinja2 template evaluation
  - Context scopes (global, pipeline, pipe)
  - Validation and dependency resolution
  - Implementation references

- **[Plugin System](plugins.md)** - Architectural overview of the plugin system:
  - Modular design and extensibility principles
  - Plugin discovery via entry points
  - Registration and integration process
  - API compatibility and versioning
  - Service and pipe registration
  - Plugin lifecycle management
  - Design principles and benefits

## When to Read This

Read the concepts documentation when you want to:
- Understand the overall architecture
- Learn about core design patterns
- Get theoretical background on system components
- Make informed decisions about extending the system

## Related Documentation

For practical guides and tutorials, see:
- [Guides](../guides/) - Step-by-step tutorials
- [Configuration](../details/configuration/) - Configuration reference
- [Code](../developers/code/) - Technical implementation details
- [Plugins](../plugins/) - Plugin development
