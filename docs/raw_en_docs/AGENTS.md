Follow this directory structure!

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
    NEW PLUGINS THAT ARE ADDED SHOULD HAVE THEIR OWN DOCS HERE
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
    OTHER INTEGRATIONS SHOULD HAVE THEIR OWN DOCS HERE
└── guides/                             # User guides and tutorials
    ├── quick_start.md                  # Getting started guide
    ├── installation.md                 # Installation instructions
    ├── first_pipeline.md               # Creating your first pipeline
    ├── testing.md                      # Testing guide
    └── troubleshooting.md              # Common issues and solutions
    OTHER GUIDES AS NEEDED