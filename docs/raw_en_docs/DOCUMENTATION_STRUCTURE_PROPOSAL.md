# English Documentation Structure Proposal

This document proposes an organized directory structure and recommended files for the English documentation in Open Ticket AI. The structure reflects the core concepts of the project: pipeline, configuration, dependency injection, and plugins.

## Proposed Directory Structure

```
docs/raw_en_docs/en/
├── README.md                           # High-level introduction to Open Ticket AI
├── code/                               # Core code concepts and architecture
│   ├── pipeline.md                     # Pipeline system overview and concepts
│   ├── orchestrator.md                 # Orchestrator functionality and scheduling
│   ├── pipe.md                         # Individual pipe components and lifecycle
│   ├── pipe_factory.md                 # Pipe instantiation and registration
│   ├── context.md                      # Pipeline execution context
│   ├── dependency_injection.md         # DI container and service registration
│   ├── services.md                     # Core services and their roles
│   └── template_rendering.md           # Jinja2 template system
├── plugins/                            # Plugin system and available plugins
│   ├── plugin_system.md                # Plugin architecture and API
│   ├── plugin_development.md           # How to develop custom plugins
│   ├── hf_local.md                     # HuggingFace local inference plugin
│   └── otobo_znuny.md                  # OTOBO/Znuny integration plugin
├── configuration/                      # Configuration system and schemas
│   ├── config_schema.md                # Configuration schema reference
│   ├── config_structure.md             # YAML structure and organization
│   ├── examples.md                     # Configuration examples overview
│   ├── defs_and_anchors.md             # Reusable definitions and YAML anchors
│   └── environment_variables.md        # Environment variable reference
├── integration/                        # External system integration
│   ├── ticket_systems.md               # Ticket system adapter architecture
│   ├── otobo_znuny_integration.md      # OTOBO/Znuny specific integration
│   ├── custom_adapters.md              # Building custom ticket system adapters
│   └── api_compatibility.md            # Plugin API versioning and compatibility
└── guides/                             # User guides and tutorials
    ├── quick_start.md                  # Getting started guide
    ├── installation.md                 # Installation instructions
    ├── first_pipeline.md               # Creating your first pipeline
    ├── testing.md                      # Testing guide
    └── troubleshooting.md              # Common issues and solutions
```

## File Descriptions

### Root Level

#### `README.md`
High-level introduction to Open Ticket AI including:
- Project overview and goals
- Key features and capabilities
- Quick links to major documentation sections
- Installation quick start
- Community and support links

### Code Section

Core architecture and implementation concepts:

#### `pipeline.md`
- Pipeline system overview
- How pipelines execute
- Pipeline lifecycle and state management
- Working with PipeResult objects

#### `orchestrator.md`
- Orchestrator role and responsibilities
- Scheduling and execution model
- Schedule configuration (`run_every_milli_seconds`)
- Pipeline supervision and error handling

#### `pipe.md`
- What is a pipe?
- Pipe interface and contract
- Input/output handling
- Stateless execution model
- Built-in pipe types

#### `pipe_factory.md`
- Pipe instantiation process
- Pipe registration and discovery
- Factory pattern implementation
- Custom pipe creation

#### `context.md`
- Execution context concept
- Sharing data between pipes
- Context lifecycle
- Best practices for context usage

#### `dependency_injection.md`
- DI container overview
- Service registration and resolution
- UnifiedRegistry usage
- Injecting services into pipes

#### `services.md`
- Core service types
- Service lifecycle management
- Creating custom services
- Service best practices

#### `template_rendering.md`
- Jinja2 template system
- Template expressions in configuration
- Custom template extensions
- Template context and variables

### Plugins Section

Plugin system and available plugins:

#### `plugin_system.md`
- Plugin architecture overview
- Plugin discovery mechanism
- Entry points system
- Plugin API versioning

#### `plugin_development.md`
- Creating a new plugin
- Plugin interface requirements
- Registering services and pipes
- Plugin packaging and distribution
- Testing plugins

#### `hf_local.md`
- HuggingFace local inference plugin
- Model loading and caching
- Supported model types
- Configuration examples
- Performance considerations

#### `otobo_znuny.md`
- OTOBO/Znuny integration plugin
- Ticket system adapter implementation
- Authentication and connection
- Supported operations
- Configuration examples

### Configuration Section

Configuration system documentation:

#### `config_schema.md`
- Complete configuration schema reference
- RawOpenTicketAIConfig structure
- Field types and validation
- Required vs optional fields

#### `config_structure.md`
- YAML structure overview
- Main configuration sections (plugins, general_config, defs, orchestrator)
- Configuration organization best practices
- Multi-environment configuration

#### `examples.md`
- Overview of available examples
- Queue classification example
- Priority classification example
- Complete workflow example
- Custom pipe examples

#### `defs_and_anchors.md`
- YAML anchors and aliases
- Reusable definitions in `defs` section
- Merging definitions with `<<: *anchor`
- Best practices for reusable configuration

#### `environment_variables.md`
- Environment variable reference
- Required variables
- Optional configuration overrides
- Security best practices

### Integration Section

External system integration:

#### `ticket_systems.md`
- Ticket system adapter architecture
- Adapter interface and contract
- Fetching and updating tickets
- Search criteria and filtering
- Error handling

#### `otobo_znuny_integration.md`
- Detailed OTOBO/Znuny integration guide
- API authentication
- Ticket operations
- Custom field handling
- Known limitations

#### `custom_adapters.md`
- Building custom ticket system adapters
- Implementing the adapter interface
- Testing custom adapters
- Packaging and distribution

#### `api_compatibility.md`
- Plugin API versioning
- Compatibility matrix
- Breaking changes policy
- Migration guides

### Guides Section

User-facing guides and tutorials:

#### `quick_start.md`
- 5-minute quick start
- Installation steps
- First configuration
- Running your first pipeline
- Next steps

#### `installation.md`
- Detailed installation instructions
- Core package installation
- Plugin installation
- Bundle installation
- Development setup

#### `first_pipeline.md`
- Step-by-step tutorial for creating a pipeline
- Understanding configuration sections
- Adding pipes to pipeline
- Testing and debugging
- Common patterns

#### `testing.md`
- Testing overview
- Unit tests
- Integration tests
- Contract tests
- E2E tests
- Running test suite

#### `troubleshooting.md`
- Common issues and solutions
- Debugging techniques
- Log analysis
- Performance optimization
- Getting help

## Implementation Notes

### Organization Principles

1. **Logical Grouping**: Files are organized by major concepts (code, plugins, configuration, integration)
2. **Progressive Disclosure**: Start with high-level concepts, then drill into details
3. **Separation of Concerns**: Keep code documentation separate from user guides
4. **Clear Naming**: File names directly reflect their content
5. **Cross-referencing**: Liberal use of links between related documents

### Migration Strategy

This proposal suggests creating a new `en/` subdirectory within `docs/raw_en_docs/` to organize all English documentation. Existing documentation files can be:

1. **Moved** to appropriate new locations
2. **Consolidated** where multiple files cover similar topics
3. **Split** where single files cover multiple distinct topics
4. **Updated** with cross-references to related documentation

### Maintenance

- Keep documentation synchronized with code changes
- Update configuration examples when schema changes
- Review and update all sections during major releases
- Ensure cross-references remain valid

## Excluded Items

This proposal explicitly **excludes**:
- Non-English documentation directories (de/, fr/, etc.)
- VitePress-specific structure (handled separately in `docs/vitepress_docs/`)
- Internal development notes (kept in `docs/internal_docs/`)
- Auto-generated API documentation (handled by separate tooling)

## Next Steps

1. Review and approve this structure
2. Create directory structure
3. Migrate existing documentation files
4. Write new documentation for gaps
5. Establish documentation review process
6. Set up automated checks for broken links
