# AI Agent Guidelines for /docs Folder

**Location:** `/docs` directory in Open Ticket AI repository  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Last Updated:** 2025-10-11

## Quick Reference

| Directory | Purpose | AI Task |
|-----------|---------|---------|
| `/docs_src/en/` | **PRIMARY SOURCE** - English documentation | Edit high-quality, ready documentation here |
| `/docs_src/{de,es,fr}/` | **AUTO-GENERATED** - Translated docs | ⚠️ DO NOT EDIT - Auto-translated from English |
## Purpose

The `/docs` folder contains **all documentation** for the Open Ticket AI project:

1. **End-user documentation** - Installation, configuration, usage guides
2. **Developer documentation** - Architecture, API reference, testing
3. **Visual diagrams** - Pipeline flows, system architecture
4. **Configuration examples** - Real-world YAML configurations (legacy)
5. **Plugin documentation** - HuggingFace local, OTOBO/Znuny integrations (legacy)
6. **Multilingual website** - VitePress-based documentation site (EN, DE, ES, FR)

## ⚠️ CRITICAL: Documentation Workflow

### Where to Write Documentation

**High-quality, ready documentation MUST be written to:**
```
/docs/vitepress_docs/docs_src/en/docs/
```

This is the **authoritative source** for all documentation. The structure is:

```
docs/docs_src/
├── en/                          # ✅ EDIT THIS - English source
│   ├── docs/
│   │   ├── concepts/           # ✨ NEW - Core concepts & architecture
│   │   ├── guides/             # HOW-TO tutorials and guides
│   │   ├── details/            # Technical details & configuration
│   │   ├── developers/         # Developer documentation
│   │   └── plugins/            # Plugin system
│   ├── products/               # Product-specific docs
│   └── blog/                   # Blog posts and articles
│
├── de/                         # ❌ DO NOT EDIT - Auto-translated German
├── es/                         # ❌ DO NOT EDIT - Auto-translated Spanish
└── fr/                         # ❌ DO NOT EDIT - Auto-translated French
```

### Translation Workflow

The translation directories (`de/`, `es/`, `fr/`) are **automatically generated** by the translation script:

**NEVER edit translation directories directly** - your changes will be overwritten!

## Three-Layer Documentation Strategy

Open Ticket AI uses a three-layer documentation approach to organize content effectively:

### 1. `concepts/` - Foundational Knowledge & Architecture

**Purpose:** Architectural overviews and core concepts that explain *what* and *why*

**Content:**
- Pipeline architecture and execution model
- Pipe system and lifecycle
- Rendering engine and template system
- Dependency injection container
- Context and state management
- Core design patterns and principles

**When to use:**
- Explaining fundamental architecture
- Describing system design decisions
- Providing theoretical background
- Documenting core abstractions

**Examples:**
```
docs/vitepress_docs/docs_src/en/docs/concepts/
├── README.md                    # Concepts directory overview
└── pipeline-architecture.md     # Complete pipeline system architecture
```

### 2. `guides/` - Practical How-To Tutorials

**Purpose:** Step-by-step instructions on *how* to accomplish specific tasks

**Content:**
- Getting started guides
- Installation instructions
- Configuration tutorials
- Common use case walkthroughs
- Troubleshooting guides
- Best practices

**When to use:**
- Writing task-oriented tutorials
- Providing step-by-step instructions
- Showing practical examples
- Helping users solve specific problems

**Examples:**
```
docs/vitepress_docs/docs_src/en/docs/guides/
├── quick_start.md              # Getting started
├── installation.md             # Setup instructions
├── first_pipeline.md           # Creating your first pipeline
├── troubleshooting.md          # Common issues and solutions
└── testing.md                  # Testing guide
```

### 3. `code/`, `configuration/`, `plugins/` - Technical Reference

**Purpose:** Detailed technical documentation for developers extending the system

**Content:**
- API references
- Code architecture details
- Configuration schemas
- Plugin development guides
- Extension points

**When to use:**
- Documenting APIs
- Explaining implementation details
- Providing reference material
- Guiding developers building extensions

**Examples:**
```
docs/vitepress_docs/docs_src/en/docs/
├── code/                       # Code architecture
│   ├── dependency_injection.md
│   ├── logging.md
│   ├── services.md
│   └── template_rendering.md
├── details/                    # Technical details
│   ├── config_reference.md     # Complete config schema reference
│   └── configuration/          # Configuration guides
│       ├── config_structure.md
│       ├── defs_and_anchors.md
│       ├── environment_variables.md
│       └── examples.md
└── plugins/                    # Plugin development
    ├── plugin_system.md
    └── plugin_development.md
```

## Decision Tree: Where to Place Documentation

Use this decision tree to choose the right location for your documentation:

```
┌─────────────────────────────────────────────┐
│ What are you documenting?                   │
└─────────────┬───────────────────────────────┘
              │
              ├─ Explaining WHY/WHAT? (Architecture, design, theory)
              │  └──> docs/concepts/
              │
              ├─ Showing HOW? (Tutorial, walkthrough, guide)
              │  └──> docs/guides/
              │
              ├─ API Reference? (Code details, schemas)
              │  └──> docs/code/, docs/configuration/, or docs/plugins/
              │
              └─ Internal development notes?
                 └──> /docs/internal_docs/
```



## Critical Information for AI Agents

### 1. Documentation Sources

**PRIMARY SOURCE**: `/docs/vitepress_docs/docs_src/en/` contains the **authoritative** English documentation.

- When users ask about "the documentation", refer to `/docs/vitepress_docs/docs_src/en/`
- Always edit `/docs/vitepress_docs/docs_src/en/` for documentation changes
- **NEVER** edit `de/`, `es/`, or `fr/` directories - they are auto-generated and will be overwritten
- The `raw_en_docs/` directory is **deprecated** and should not be used for new documentation

### 2. The `concepts/` Directory - New Addition

The `concepts/` directory is a **new addition** to the documentation structure:

**Location:** `/docs/vitepress_docs/docs_src/en/docs/concepts/`

**Purpose:** Provide architectural overviews and foundational knowledge

**What belongs in `concepts/`:**
- Pipeline architecture and how it works
- Pipe system design and execution model
- Rendering engine internals
- Dependency injection container architecture
- Core design patterns and abstractions
- Theoretical background and design decisions

**What does NOT belong in `concepts/`:**
- Step-by-step tutorials (use `guides/`)
- API reference details (use `code/`, `configuration/`, or `plugins/`)
- Troubleshooting guides (use `guides/`)

**Navigation:** The VitePress navigation will automatically include `concepts/` when files are added to this directory.

### 3. Configuration Examples

Configuration examples can be found in the legacy `raw_en_docs/config_examples/` directory. These may be migrated to the new structure in the future.

**Key files for configuration help:**
- `raw_en_docs/config_examples/complete_workflow.yml` - Comprehensive example
- `raw_en_docs/config_examples/queue_classification.yml` - Queue routing pattern
- `raw_en_docs/config_examples/QUICK_REFERENCE.md` - Quick comparison table

### 4. Architecture Understanding

**Read these for system understanding:**

1. **`diagrams/pipeline_flow.md`** - Mermaid diagram showing pipeline execution
2. **`diagrams/architecture_overview.puml`** - PlantUML system architecture
3. **`docs/vitepress_docs/docs_src/en/docs/concepts/`** - Architectural concepts (when populated)

### 5. Pipe Documentation (man_structured/)

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

### 6. Multilingual Support (VitePress)

Supported languages: **EN** (English), **DE** (German), **ES** (Spanish), **FR** (French)

**Critical workflow:**
1. ✅ **ALWAYS** edit English first: `/docs/vitepress_docs/docs_src/en/`
2. ❌ **NEVER** edit translation directories directly: `de/`, `es/`, `fr/`
3. 🔄 Translations are auto-generated by running: `uv run python python_extras/scripts/translate_documentation.py translate`
4. Each language has a `messages.ts` file for UI strings
5. The translation script will overwrite any manual changes in translation directories

## Guidelines for AI Agents

### When Reading Documentation

1. **Start with the new structure** - `/docs/vitepress_docs/docs_src/en/docs/`
2. **Check `concepts/`** - For architectural understanding (when populated)
3. **Review `guides/`** - For practical examples and tutorials
4. **Reference diagrams** - Visual understanding in `/docs/diagrams/`
5. **Legacy docs** - `raw_en_docs/` may have useful info but is deprecated

### When Editing Documentation

1. ✅ **DO** edit `/docs/vitepress_docs/docs_src/en/` for all documentation changes
2. ✅ **DO** use the three-layer strategy: `concepts/`, `guides/`, or technical reference
3. ✅ **DO** follow the decision tree to choose the right location
4. ✅ **DO** follow existing Markdown structure and formatting
5. ✅ **DO** add examples and code snippets for clarity
6. ❌ **DON'T** edit translation directories (`de/`, `es/`, `fr/`) - they are auto-generated
7. ❌ **DON'T** edit `raw_en_docs/` - it is deprecated
8. ❌ **DON'T** break existing links or references
9. ❌ **DON'T** remove examples without replacement

### When Creating New Documentation

1. **Choose the right layer** (use the decision tree above):
   - Architecture/theory → `docs/concepts/`
   - Tutorial/guide → `docs/guides/`
   - API/reference → `docs/code/`, `docs/configuration/`, or `docs/plugins/`
   - Diagram → `/docs/diagrams/`
   - Internal notes → `/docs/internal_docs/`

2. **Follow naming conventions:**
   - Use lowercase with hyphens: `pipeline-architecture.md` not `Pipeline_Architecture.md`
   - Be descriptive: `troubleshooting-common-errors.md` not `errors.md`

3. **Add frontmatter metadata:**
   ```markdown
   ---
   title: Page Title
   description: SEO-friendly description
   ---
   ```

4. **Structure content clearly:**
   - Start with a clear introduction
   - Use headings hierarchically (h2 → h3 → h4)
   - Add code examples where appropriate
   - Include cross-references to related docs

### When Creating `concepts/` Documentation

The `concepts/` directory is for **architectural and theoretical content**:

**Good examples for `concepts/`:**
- "How the Pipeline Architecture Works" - explains the overall design
- "Pipe Lifecycle and Execution Model" - describes the abstraction
- "Dependency Injection in Open Ticket AI" - explains the pattern
- "Context and State Management" - describes the concept

**Bad examples for `concepts/` (use `guides/` instead):**
- "How to Create Your First Pipeline" - this is a tutorial
- "Configuring the Orchestrator" - this is a how-to guide
- "Troubleshooting Pipeline Errors" - this is a guide

**Writing style for `concepts/`:**
- Focus on "what" and "why" rather than "how"
- Explain design decisions and trade-offs
- Use diagrams to illustrate architecture
- Link to practical guides for implementation

### When Helping with Configuration

1. **Reference legacy examples** - Point users to `raw_en_docs/config_examples/` (until migrated)
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
   - Place in `/docs/diagrams/`

2. **Mermaid diagrams** (`.md` with mermaid code blocks):
   - Use for flowcharts, sequence diagrams, state diagrams
   - Embed in Markdown with ` ```mermaid ` blocks
   - Add descriptive text around the diagram
   - Can be placed in `/docs/diagrams/` or inline in documentation

3. **Always include**:
   - Title/heading
   - Brief description of what the diagram shows
   - Legend if using custom symbols/colors

## Migration from Legacy Documentation

The `raw_en_docs/` directory is being phased out. When you encounter content that needs to be updated:

1. **If content is high quality and ready:**
   - Migrate it to the appropriate location in `/docs/vitepress_docs/docs_src/en/docs/`
   - Use the three-layer strategy to choose the right location
   - Update any links that reference the old location

2. **If content needs work:**
   - Leave it in `raw_en_docs/` for now
   - Note that it needs migration in your response

3. **Do not:**
   - Create new content in `raw_en_docs/`
   - Extensively edit content in `raw_en_docs/` unless specifically asked

## Common Tasks

### Adding New Conceptual Documentation

1. Create a new file in `/docs/vitepress_docs/docs_src/en/docs/concepts/`
2. Use descriptive filename: `pipeline-architecture.md`
3. Add frontmatter with title and description
4. Write content focusing on "what" and "why"
5. Link to related guides for "how to" instructions
6. Navigation will be automatically generated by VitePress

### Adding a New Tutorial or Guide

1. Create a new file in `/docs/vitepress_docs/docs_src/en/docs/guides/`
2. Use descriptive filename: `creating-custom-pipes.md`
3. Add frontmatter with title and description
4. Write step-by-step instructions
5. Include code examples and expected outputs
6. Add troubleshooting section if applicable

### Adding Technical Reference Documentation

1. Determine the right subdirectory:
   - Code architecture → `/docs/vitepress_docs/docs_src/en/docs/code/`
   - Configuration schema → `/docs/vitepress_docs/docs_src/en/docs/details/config_reference.md`
   - Configuration guides → `/docs/vitepress_docs/docs_src/en/docs/details/configuration/`
   - Plugins → `/docs/vitepress_docs/docs_src/en/docs/plugins/`
2. Create or update the relevant file
3. Document APIs, schemas, and technical details
4. Include code examples and type information

### Creating a New Diagram

1. Choose format: PlantUML (`.puml`) or Mermaid (`.md`)
2. Create file in `/docs/diagrams/` directory
3. Use descriptive filename: `pipe-lifecycle-flow.md`
4. Include title and description
5. Reference from relevant documentation in `docs_src/en/`

### Updating Translations

**DO NOT** edit translation directories manually. Instead:

1. Edit the English source: `/docs/vitepress_docs/docs_src/en/`
2. Run the translation script:
   ```bash
   uv run python python_extras/scripts/translate_documentation.py translate
   ```
3. The script will automatically update `de/`, `es/`, and `fr/` directories

## Project Core Concepts (Quick Reference)

Understanding these concepts helps when writing documentation:

1. **Pipeline**: Ordered execution of pipes with context sharing
2. **Orchestrator**: Manages pipeline scheduling and execution
3. **Pipe**: Individual processing unit (fetch, transform, classify, update)
4. **Context**: Shared state across pipeline execution (`context.pipes[id]`)
5. **PipeFactory**: Creates pipe instances with dependency injection
6. **Dependency Injection**: Service container for adapters, models, etc.
7. **Template Rendering**: Jinja2 templating in configuration
8. **Plugin System**: Extensible architecture for integrations and ML models

## Documentation Best Practices

### DO:
1. ✅ Write clear, concise documentation with examples
2. ✅ Use the three-layer strategy (concepts/guides/reference)
3. ✅ Add code examples that users can copy and run
4. ✅ Include diagrams for complex concepts
5. ✅ Link to related documentation
6. ✅ Add frontmatter metadata for SEO
7. ✅ Test all code examples before publishing
8. ✅ Use the decision tree to choose the right location

### DON'T:
1. ❌ Edit translation directories (`de/`, `es/`, `fr/`) directly
2. ❌ Create new documentation in `raw_en_docs/`
3. ❌ Mix conceptual and tutorial content in the same document
4. ❌ Duplicate content across multiple locations
5. ❌ Break existing links when moving/updating docs
6. ❌ Remove examples without providing alternatives
7. ❌ Use absolute paths that will break when structure changes
8. ❌ Forget to add descriptive titles and metadata

## VitePress Navigation

The VitePress navigation is automatically generated from the directory structure. When you add new files to:
- `/docs/vitepress_docs/docs_src/en/docs/concepts/`
- `/docs/vitepress_docs/docs_src/en/docs/guides/`
- `/docs/vitepress_docs/docs_src/en/docs/code/`
- etc.

The navigation will automatically include them. No manual configuration is needed.

**Navigation configuration:** `/docs/vitepress_docs/.vitepress/config.mts`

## Testing Documentation Changes

Before committing documentation:

1. **Verify Markdown syntax** - Ensure proper formatting
2. **Test code examples** - Run all code snippets to ensure they work
3. **Check links** - Verify all internal and external links
4. **Preview locally** - Run VitePress dev server to see how it renders:
   ```bash
   cd docs/vitepress_docs
   npm run docs:dev
   ```
5. **Review structure** - Ensure content is in the right layer (concepts/guides/reference)

## Questions to Ask When Unsure

1. "Is this explaining WHY/WHAT (concepts) or HOW (guides)?"
2. "Should this go in concepts/, guides/, or technical reference?"
3. "Am I editing the English source or a translation directory?"
4. "Does this belong in the new structure or is it legacy content?"
5. "Should this be a diagram or written documentation?"

## Summary: Key Takeaways

🎯 **Primary Documentation Location:**
- `/docs/vitepress_docs/docs_src/en/` is the authoritative source
- All new documentation goes here

🚫 **Never Edit:**
- Translation directories (`de/`, `es/`, `fr/`) - auto-generated
- `raw_en_docs/` - deprecated legacy documentation

📚 **Three-Layer Strategy:**
- `concepts/` - Architecture and theory (what/why)
- `guides/` - Tutorials and how-tos (how)
- `code/`/`configuration/`/`plugins/` - Technical reference (API docs)

🤖 **For AI Agents:**
- Use the decision tree to choose documentation location
- Follow the three-layer strategy
- Never edit auto-generated translations
- Test all code examples before committing

---

**Remember**: Good documentation is clear, well-organized, and easy to find. Use the three-layer strategy to ensure users can quickly locate the information they need.

