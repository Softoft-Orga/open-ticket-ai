# AI Agent Guidelines for /docs Folder

**Location:** `C:\Users\PC\PycharmProjects\open-ticket-ai\docs`  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Last Updated:** 2025-10-09

## Quick Reference

| Directory | Purpose | AI Task |
|-----------|---------|---------|
| `raw_en_docs/` | Source English documentation (Markdown) | Read for project concepts, edit for doc updates |
| `vitepress_docs/` | VitePress website source (multilingual) | Frontend docs, i18n content |
| `diagrams/` | Architecture diagrams (PlantUML, Mermaid) | Visual documentation, flow diagrams |
| `man_structured/` | Structured pipe reference (YAML sidecar files) | API documentation for pipes |
| `internal_docs/` | Internal development notes | Project structure guidelines |

## Purpose

The `/docs` folder contains **all documentation** for the Open Ticket AI project:

1. **End-user documentation** - Installation, configuration, usage guides
2. **Developer documentation** - Architecture, API reference, testing
3. **Visual diagrams** - Pipeline flows, system architecture
4. **Configuration examples** - Real-world YAML configurations
5. **Plugin documentation** - HuggingFace local, OTOBO/Znuny integrations
6. **Multilingual website** - VitePress-based documentation site (EN, DE, ES, FR)

## Directory Structure

```
docs/
├── AGENTS.md                        # THIS FILE - AI guidelines for docs
├── diagrams/                        # Architecture & flow diagrams
│   ├── architecture_overview.puml   # PlantUML system architecture
│   ├── pipeline_flow.md             # Mermaid pipeline execution flow
│   ├── otobo_demo_*.md              # OTOBO integration diagrams
│   └── *.puml                       # Other PlantUML diagrams
│
├── internal_docs/                   # Internal development notes
│   ├── AGENTS_STRUCTURE.md          # Template for AGENTS.md files
│   └── note.md                      # Development notes
│
├── man_structured/                  # Structured API reference
│   └── pipes/                       # Pipe documentation (YAML sidecar files)
│       ├── sidecar_pipe_schema.yml  # Schema definition
│       ├── add_note_pipe.sidecar.yml
│       ├── fetch_tickets_pipe.sidecar.yml
│       ├── update_ticket_pipe.sidecar.yml
│       ├── jinja_expression_pipe.sidecar.yml
│       └── default_pipe.sidecar.yml
│
├── raw_en_docs/                     # **PRIMARY SOURCE** English docs
│   ├── README.md                    # Main project README
│   ├── DOCUMENTATION_STRUCTURE.md   # Proposed doc organization
│   ├── _documentation_summaries.json # AI-friendly doc summaries
│   ├── AGENTS.md                    # Additional AI guidelines
│   ├── RELEASE.md                   # Release process
│   │
│   ├── config_examples/             # **CRITICAL** YAML configuration examples
│   │   ├── README.md                # Examples overview
│   │   ├── QUICK_REFERENCE.md       # Quick comparison table
│   │   ├── AGENTS.md                # AI guidelines for config examples
│   │   ├── queue_classification.yml # Queue routing example
│   │   ├── priority_classification.yml
│   │   ├── add_note_when_in_queue.yml
│   │   ├── create_ticket_on_condition.yml
│   │   └── complete_workflow.yml    # Comprehensive example
│   │
│   ├── general/                     # General guides
│   │   ├── README.md
│   │   ├── QUICK_START.md
│   │   ├── SETUP_INSTRUCTIONS.md
│   │   ├── CI_QUALITY_ASSURANCE.md
│   │   ├── ISSUE_TEMPLATES.md
│   │   └── testing/                 # Testing documentation
│   │       ├── contract_tests.md
│   │       ├── e2e_tests.md
│   │       ├── integration_tests.md
│   │       └── test_data.md
│   │
│   ├── open_ticket_ai/              # Core package docs
│   │   ├── CLI_USAGE.md
│   │   └── predefined-pipes.md
│   │
│   ├── otai_hf_local/               # HuggingFace plugin docs
│   │   ├── README.md
│   │   ├── PLUGIN_HF_LOCAL_README.md
│   │   ├── CHANGELOG.md
│   │   ├── LICENSE
│   │   └── RELEASE.md
│   │
│   └── otai_otobo_znuny/            # OTOBO/Znuny plugin docs
│       ├── README.md
│       ├── PLUGIN_OTOBO_ZNUNY_README.md
│       ├── CHANGELOG.md
│       ├── LICENSE
│       └── RELEASE.md
│
└── vitepress_docs/                  # VitePress website source
    ├── package.json
    ├── tailwind.config.cjs
    ├── postcss.config.cjs
    │
    ├── docs_src/                    # Multilingual documentation
    │   ├── en/                      # English (primary)
    │   │   ├── index.md
    │   │   ├── messages.ts          # i18n messages
    │   │   ├── blog/                # Blog posts
    │   │   ├── guide/               # User guides
    │   │   ├── developers/          # Developer docs
    │   │   ├── products/            # Product docs
    │   │   └── _config_examples/    # Config examples for web
    │   ├── de/                      # German
    │   ├── es/                      # Spanish
    │   ├── fr/                      # French
    │   └── public/                  # Static assets
    │
    ├── stories/                     # Storybook component stories
    │   ├── Button.stories.ts
    │   ├── Card.stories.ts
    │   └── *.stories.ts
    │
    └── netlify/                     # Netlify deployment
        └── functions/
```

## Critical Information for AI Agents

### 1. Documentation Sources

**PRIMARY SOURCE**: `raw_en_docs/` contains the **authoritative** English documentation.

- When users ask about "the documentation", refer to `raw_en_docs/`
- `vitepress_docs/docs_src/en/` is generated/synced from `raw_en_docs/` (web version)
- Always edit `raw_en_docs/` first, then sync to VitePress if needed

### 2. Configuration Examples Location

**CRITICAL**: Configuration examples are in `raw_en_docs/config_examples/`

These YAML files demonstrate:
- Pipeline configuration structure
- Dependency injection setup
- Pipe chaining and orchestration
- Conditional execution (`if` conditions)
- Template rendering (Jinja2)
- Ticket system integration

**Key files to reference when helping with configuration:**
- `complete_workflow.yml` - Comprehensive multi-step example
- `queue_classification.yml` - Queue routing pattern
- `priority_classification.yml` - Priority assignment pattern
- `add_note_when_in_queue.yml` - Conditional note addition
- `QUICK_REFERENCE.md` - Quick comparison of all examples

### 3. Architecture Understanding

**Read these for system understanding:**

1. **`diagrams/pipeline_flow.md`** - Mermaid diagram showing:
   - Initialization phase
   - Orchestrator loop
   - Pipe processing (simple vs composite)
   - Context updates and result persistence

2. **`diagrams/architecture_overview.puml`** - PlantUML system architecture

3. **`raw_en_docs/DOCUMENTATION_STRUCTURE.md`** - Proposed documentation organization with:
   - Core concepts: pipeline, orchestrator, pipe, context, DI
   - Plugin architecture
   - Integration patterns

### 4. Pipe Documentation (man_structured/)

The `man_structured/pipes/` directory contains **YAML sidecar files** that document each pipe:

**Schema structure:**
```yaml
_class: fully.qualified.ClassName
_extends: base.class.Name
_title: {en: "...", de: "..."}  # i18n titles
_summary: {en: "...", de: "..."}  # i18n summaries
_category: category-name
_inputs:
  config: ConfigClassName
  params: {param_name: {en: "...", de: "..."}}
_defaults: {param: value}
_output:
  state_enum: [ok, skipped, failed]
  payload_schema_ref: Schema.Reference
  examples: {ok: {...}, skipped: {...}, failed: {...}}
_errors:
  fail: [{code: error_code, when: {en: "...", de: "..."}}]
```

**When documenting a new pipe:**
1. Create a `.sidecar.yml` file in `man_structured/pipes/`
2. Follow the schema from `sidecar_pipe_schema.yml`
3. Provide bilingual (EN/DE) descriptions
4. Document all input parameters and outputs
5. Include example payloads for each state

### 5. Plugin Documentation Pattern

Each plugin follows this structure:
```
otai_<plugin_name>/
├── README.md                    # User-facing overview
├── PLUGIN_<NAME>_README.md      # Detailed plugin documentation
├── CHANGELOG.md                 # Version history
├── LICENSE                      # License file
└── RELEASE.md                   # Release process
```

**When adding a new plugin:**
1. Create a new directory under `raw_en_docs/`
2. Follow the naming convention: `otai_<plugin_name>/`
3. Include all standard files (README, PLUGIN_README, CHANGELOG, LICENSE)
4. Update `DOCUMENTATION_STRUCTURE.md` to reference the new plugin
5. Add integration docs to the integration section

### 6. Version Compatibility Information

From `raw_en_docs/README.md`:

| Core Version | Plugin API | HF Local | OTOBO/Znuny | Status |
|--------------|-----------|----------|-------------|--------|
| 1.0.0rc1     | 2.0       | 1.0.0rc1 | 1.0.0rc1    | Beta   |
| 1.x.x        | 2.0       | 1.x.x    | 1.x.x       | Compatible |

Plugins declare compatibility via dependency ranges (e.g., `open-ticket-ai>=1.0.0,<2.0.0`)

### 7. Multilingual Support (VitePress)

Supported languages: **EN** (English), **DE** (German), **ES** (Spanish), **FR** (French)

- English is the primary language
- Each language has its own directory in `vitepress_docs/docs_src/`
- `messages.ts` files contain i18n message keys
- Always update English first, then other languages

## Guidelines for AI Agents

### When Reading Documentation

1. **Start with `_documentation_summaries.json`** - AI-friendly summaries of all major docs
2. **Check `DOCUMENTATION_STRUCTURE.md`** - Understand the proposed organization
3. **Read relevant config examples** - They show real-world usage patterns
4. **Review diagrams** - Visual understanding of pipeline execution and architecture

### When Editing Documentation

1. ✅ **DO** edit `raw_en_docs/` for content changes
2. ✅ **DO** update both EN and DE versions when possible
3. ✅ **DO** follow the existing Markdown structure and formatting
4. ✅ **DO** add examples and code snippets for clarity
5. ✅ **DO** update `_documentation_summaries.json` for major changes
6. ❌ **DON'T** edit `vitepress_docs/` directly without updating `raw_en_docs/`
7. ❌ **DON'T** break existing links or references
8. ❌ **DON'T** remove examples without replacement

### When Creating New Documentation

1. Determine the appropriate directory:
   - User guides → `raw_en_docs/general/` or `raw_en_docs/guides/`
   - Config examples → `raw_en_docs/config_examples/`
   - Plugin docs → `raw_en_docs/otai_<plugin_name>/`
   - Developer docs → `raw_en_docs/developers/` or create new section
   - Diagrams → `diagrams/`

2. Follow the existing naming conventions:
   - Use lowercase with underscores or hyphens
   - Be descriptive: `priority_classification.yml` not `config1.yml`

3. Add metadata where appropriate:
   - Title, summary, and description
   - Date created/updated
   - Related documents

### When Helping with Configuration

1. **Reference the examples**: Point users to `config_examples/`
2. **Explain the pipeline structure**:
   - `services`: Dependency injection container
   - `defs`: Reusable YAML anchors
   - `pipeline`: Ordered list of pipes to execute
3. **Show how pipes work**:
   - Each pipe has `id`, `use` (class reference), optional `if` (condition)
   - Pipes can reference outputs from previous pipes via `context.pipes.pipe_id`
   - Template rendering uses Jinja2: `{{ variable }}`, `{% if %}`, etc.
4. **Explain dependencies**:
   - `depends_on`: List of pipe IDs that must run first
   - Results stored in `context.pipes[pipe_id]`

### When Documenting Diagrams

1. **PlantUML files** (`.puml`):
   - Use for class diagrams, component diagrams, deployment diagrams
   - Follow PlantUML syntax
   - Include comments for complex sections

2. **Mermaid diagrams** (`.md` with mermaid code blocks):
   - Use for flowcharts, sequence diagrams, state diagrams
   - Embed in Markdown with ````mermaid` blocks
   - Add descriptive text around the diagram

3. **Always include**:
   - Title/heading
   - Brief description of what the diagram shows
   - Legend if using custom symbols/colors

## Testing Documentation

When creating or updating documentation:

1. **Verify links work** - Check all internal references
2. **Test code examples** - Ensure code snippets are valid
3. **Check YAML syntax** - Validate configuration examples
4. **Review rendering** - Preview Markdown rendering
5. **Validate against schema** - Config examples should match schema

## Common Tasks

### Adding a New Configuration Example

1. Create `raw_en_docs/config_examples/your_example.yml`
2. Add description to `raw_en_docs/config_examples/README.md`
3. Update `QUICK_REFERENCE.md` comparison table
4. Consider adding to VitePress: `vitepress_docs/docs_src/en/_config_examples/`

### Adding a New Plugin

1. Create `raw_en_docs/otai_<plugin_name>/` directory
2. Add: README.md, PLUGIN_<NAME>_README.md, CHANGELOG.md, LICENSE
3. Update `DOCUMENTATION_STRUCTURE.md` plugins section
4. Add integration guide if needed
5. Update version compatibility table in main README

### Creating a New Diagram

1. Choose format: PlantUML (`.puml`) or Mermaid (`.md`)
2. Create file in `diagrams/` directory
3. Use descriptive filename: `feature_flow_diagram.md`
4. Reference from relevant documentation

### Updating Multi-language Docs

1. Edit English version first: `vitepress_docs/docs_src/en/`
2. Update other languages: `de/`, `es/`, `fr/`
3. Update `messages.ts` files for UI strings
4. Test language switcher functionality

## Project Core Concepts (Quick Reference)

Based on `DOCUMENTATION_STRUCTURE.md`:

1. **Pipeline**: Ordered execution of pipes with context sharing
2. **Orchestrator**: Manages pipeline scheduling and execution
3. **Pipe**: Individual processing unit (fetch, transform, classify, update)
4. **Context**: Shared state across pipeline execution (`context.pipes[id]`)
5. **PipeFactory**: Creates pipe instances with DI
6. **Dependency Injection**: Service container for adapters, models, etc.
7. **Template Rendering**: Jinja2 templating in configuration
8. **Plugin System**: Extensible architecture for integrations and ML models

## Anti-Patterns to Avoid

1. ❌ **Duplicating documentation** - Sync between `raw_en_docs/` and `vitepress_docs/`
2. ❌ **Incomplete examples** - Always provide full working YAML configs
3. ❌ **Missing error documentation** - Document failure cases in sidecar files
4. ❌ **Language inconsistency** - Update all supported languages
5. ❌ **Broken internal links** - Verify all cross-references
6. ❌ **Undocumented configuration options** - Every config key needs explanation
7. ❌ **Missing type information** - Specify types for all parameters

## Resources

- **VitePress Setup**: See [VITEPRESS_SETUP.md](VITEPRESS_SETUP.md) for documentation website setup
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- **JSON Schema**: Check for `config.schema.json` in project root
- **API Reference**: See `raw_en_docs/developers/api/` for API docs
- **Testing Guides**: See `raw_en_docs/general/testing/`
- **Blog Posts**: See `vitepress_docs/docs_src/en/blog/` for tutorials

## Questions to Ask When Unsure

1. "Is this documentation for end users or developers?"
2. "Which language(s) need to be updated?"
3. "Should this sync to the VitePress website?"
4. "Are there existing examples I should follow?"
5. "Does this need diagram support?"

---

**Remember**: Documentation is code. Keep it accurate, complete, and well-organized. When in doubt, look at existing examples and follow established patterns.

