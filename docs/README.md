# Documentation Directory

This directory contains documentation for Open Ticket AI.

## Directory Structure

### `/docs/diagrams/`

Centralized location for all architecture diagrams, flowcharts, and visual documentation.

**Supported formats:**
- PlantUML (`.puml`)
- Mermaid (`.mmd`, or embedded in `.md`)
- D2 (`.d2`)
- Images (`.png`, `.svg`, `.jpg`)

**Current diagrams:**
- `architecture_overview.puml` - System architecture overview
- `class_diagram.puml` - Class hierarchy and relationships
- `dependency_injection.puml` - Dependency injection flow
- `pipeline_flow.puml` - Pipeline execution flow
- `pipeline-context.md` - Pipeline context documentation with diagrams
- `pipeline_flow.md` - Pipeline flow with mermaid diagrams
- `test-structure.md` - Test structure diagrams
- `to_mermaid_conversion.puml` - PlantUML to Mermaid conversion examples
- `to_mermaid_conversion_simple.puml` - Simple conversion examples

**Usage guidelines:**
1. Place all new diagrams in `/docs/diagrams/`
2. Use descriptive filenames (e.g., `feature-architecture.puml`)
3. Include a brief comment at the top of each diagram file describing its purpose
4. Reference diagrams from documentation using relative paths: `../diagrams/filename.ext`
5. For markdown files with embedded diagrams (mermaid), keep them in `/docs/diagrams/` if they are primarily diagram documentation

### `/docs/config_examples/`

Configuration file examples and templates.

### `/docs/raw_en_docs/`

Raw English documentation files.

### `/docs/vitepress_docs/`

VitePress documentation site source files. Do not modify diagram paths in this directory.

### `/docs/internal_docs/`

Internal documentation and notes.

## Adding New Diagrams

When adding new diagrams to the repository:

1. Save the diagram file to `/docs/diagrams/`
2. Use appropriate file extensions (`.puml`, `.d2`, `.mmd`, `.svg`, `.png`)
3. Update this README if adding a significant new diagram
4. Reference the diagram in relevant documentation files
