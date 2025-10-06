# Documentation Index

This directory contains the raw English documentation for Open Ticket AI, organized into logical subdirectories for easy navigation.

## Root Documentation Files

Essential documentation that all contributors and users should read:

- **[README.md](README.md)** - Project overview, installation, and quick start
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Complete contributor guide with development workflow
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide and best practices

## Subdirectories

### guides/

User-facing guides for setup, configuration, and usage:

- **[QUICK_START.md](guides/QUICK_START.md)** - Quick start guide for getting up and running
- **[SETUP_INSTRUCTIONS.md](guides/SETUP_INSTRUCTIONS.md)** - Detailed setup and deployment instructions
- **[CLI_USAGE.md](guides/CLI_USAGE.md)** - Command-line interface usage guide
- **[WORKSPACE_SETUP.md](guides/WORKSPACE_SETUP.md)** - Development workspace setup guide

### plugins/

Plugin development documentation:

- **[PLUGIN_STANDARDS.md](plugins/PLUGIN_STANDARDS.md)** - Complete plugin distribution standards
- **[PLUGIN_QUICK_REFERENCE.md](plugins/PLUGIN_QUICK_REFERENCE.md)** - Quick reference for plugin development
- **[PLUGIN_HF_LOCAL_README.md](plugins/PLUGIN_HF_LOCAL_README.md)** - HuggingFace local plugin documentation
- **[PLUGIN_HF_LOCAL_CHANGELOG.md](plugins/PLUGIN_HF_LOCAL_CHANGELOG.md)** - HF Local plugin changelog
- **[PLUGIN_OTOBO_ZNUNY_README.md](plugins/PLUGIN_OTOBO_ZNUNY_README.md)** - OTOBO/Znuny plugin documentation
- **[PLUGIN_OTOBO_ZNUNY_CHANGELOG.md](plugins/PLUGIN_OTOBO_ZNUNY_CHANGELOG.md)** - OTOBO/Znuny plugin changelog

### reference/

Reference documentation and policies:

- **[RELEASE.md](reference/RELEASE.md)** - Release procedures and versioning strategy
- **[DEPRECATION_POLICY.md](reference/DEPRECATION_POLICY.md)** - Deprecation guidelines and policies
- **[workflow_architecture.md](reference/workflow_architecture.md)** - PyPI publishing workflow architecture
- **[predefined-pipes.md](reference/predefined-pipes.md)** - Predefined pipe concepts and design

## Related Documentation

### Configuration Examples

Moved to `/docs/config_examples/` for better organization:
- Sample YAML configurations
- Template renderer configuration
- Workflow examples
- Quick reference guide

See [/docs/config_examples/README.md](../config_examples/README.md) for details.

### Internal Documentation

Implementation notes and internal development documentation are in `/docs/internal_docs/`:
- Implementation summaries
- Package status tracking
- Release process documentation
- Developer automation processes

These are primarily for development team reference.

### Diagrams

All architecture and technical diagrams are in `/docs/diagrams/`:
- Architecture overviews
- Pipeline flow visualizations
- Test structure diagrams

### VitePress Documentation

The user-facing documentation website is in `/docs/vitepress_docs/`:
- Multilingual documentation
- API references
- Tutorials and guides

This has its own structure and should not be modified as part of general documentation reorganization.

## Navigation Tips

- Start with **README.md** for project overview
- Read **CONTRIBUTING.md** before making code contributions
- Consult **TESTING.md** when writing or running tests
- Check **guides/** for setup and usage instructions
- See **plugins/** for plugin development
- Reference **reference/** for policies and architecture

## Contributing to Documentation

When adding new documentation:

1. Place user guides in `guides/`
2. Place plugin documentation in `plugins/`
3. Place reference documentation in `reference/`
4. Keep root files for major cross-cutting documentation only
5. Update this INDEX.md when adding new major documents
6. Follow naming conventions (UPPERCASE for major docs, lowercase_with_underscores for specific guides)
