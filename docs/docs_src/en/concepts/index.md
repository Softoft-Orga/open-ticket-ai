---
description: Explore Open Ticket AI's core architectural concepts including pipelines, configuration rendering, plugins, and versioning strategies.
---

# Core Concepts

This directory contains architectural documentation that explains the fundamental concepts and design of Open Ticket AI.

## What's in Concepts?

The concepts documentation focuses on **what** the system is and **why** it's designed that way, rather than **how** to
use it.

### Available Documentation

- **[Pipeline System](pipeline.md)** - Comprehensive guide to pipelines with diagrams explaining:
    - What pipelines are and how they work
    - Pipeline orchestration lifecycle (rendering and execution)
    - When and how pipelines are triggered and executed
    - Relationship between pipes, composite pipes, and steps
    - Mermaid architecture and sequence diagrams
    - Implementation references and best practices

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

- **[Application Flow](app_flow.md)** - Diagram illustrating the application startup and orchestration process:
    - Application bootstrap sequence
    - Dependency injection container setup
    - Orchestrator initialization and runner creation
    - Trigger setup and execution strategy
    - Visual flowchart of the complete app lifecycle

- **[Versioning Policy](versioning.md)** - Guidelines for product and documentation versioning:
    - Semantic versioning principles
    - Branching and release channel strategy
    - Documentation versioning with VitePress and Netlify
    - Version switcher UX and SEO considerations
    - Communication of changes and feature availability

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
