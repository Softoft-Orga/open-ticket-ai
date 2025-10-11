# Documentation Structure

This folder contains all documentation for the Open Ticket AI project, organized into clear subfolders for easy navigation and maintenance.

## Folder Organization

### `/docs/raw_en_docs`
Raw English documentation files for the project.

Contains:
- Contributing guidelines (CONTRIBUTING.md)
- Testing documentation (TESTING.md)
- Setup and deployment guides
- Development workflows
- Plugin standards and implementation guides
- Release and deprecation policies
- Quick start guides
- Technical implementation notes

This is the source documentation in English before any translation or processing.

### `/docs/man_structured`
Structured YAML documentation for automated processing.

Contains:
- Pipe sidecar YAML files (`.sidecar.yml`)
- Schema definitions for documentation structure
- Machine-readable metadata for pipes and components

These files are used for automated documentation generation and validation.

### `/docs/diagrams`
All architecture and technical diagrams.

Contains:
- PlantUML diagrams (`.puml`)
- Markdown-based diagrams
- Architecture overviews
- Pipeline flow visualizations
- Test structure diagrams
- Dependency injection diagrams

All visual documentation should be placed here regardless of format.

### `/docs/config_examples`
Configuration file examples and templates.

Contains:
- Sample YAML configuration files
- Template renderer configuration guides
- Quick reference for configuration
- Workflow examples (queue classification, priority classification, etc.)
- Python template extension examples

These examples help users understand how to configure the system.

### `/docs/internal_docs`
Internal development notes and planning documents.

Contains:
- Developer notes
- Implementation ideas
- Temporary planning documents

Not intended for end-users; for development team reference only.

### `/docs/vitepress_docs`
VitePress documentation site source files.

**DO NOT MODIFY** as part of general documentation reorganization.

Contains:
- VitePress configuration
- Multilingual documentation source
- Static site generation assets

This folder has its own structure and workflow for the documentation website.

## Documentation Guidelines

### Adding New Documentation

1. **User-facing guides**: Add to `/docs/raw_en_docs`
2. **Diagrams**: Add to `/docs/diagrams`
3. **Configuration examples**: Add to `/docs/config_examples`
4. **Machine-readable metadata**: Add to `/docs/man_structured`
5. **Internal notes**: Add to `/docs/internal_docs`
6. **Website documentation**: Follow VitePress guidelines in `/docs/vitepress_docs`

### File Naming Conventions

- Use UPPERCASE for major documents (e.g., README.md, CONTRIBUTING.md)
- Use lowercase with underscores for specific guides (e.g., pipeline_flow.md)
- Use descriptive names that indicate content clearly

### Avoiding Duplication

- Check existing documentation before creating new files
- Update existing documents rather than creating duplicates
- Reference other documentation files using relative paths

## Translation Workflow

All documentation starts in English in `/docs/raw_en_docs`. Translation processes should:
1. Source from `/docs/raw_en_docs`
2. Output to appropriate locations (e.g., VitePress multilingual folders)
3. Never modify the English source files during translation

## Maintenance

- Keep documentation synchronized with code changes
- Update diagrams when architecture changes
- Review and update examples when configuration schemas change
- Archive outdated documentation rather than deleting it
