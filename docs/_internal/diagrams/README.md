# Architecture Diagrams

This directory contains architecture diagrams for Open Ticket AI in multiple formats.

## Available Diagrams

### Core Architecture Overview

The core architecture overview is available in multiple formats:

- **D2 Format**: `architecture_overview.d2` - Multi-layered class diagram with interactive drill-down capabilities
- **PlantUML Format**: `architecture_overview.puml` - Traditional UML class diagram

#### D2 Architecture Diagram

The D2 diagram (`architecture_overview.d2`) provides a comprehensive, multi-layered view of the Open Ticket AI architecture:

**Main Layers:**
1. Core Pipeline Components
2. Pipeline Construction & Factory
3. Configuration System
4. Dependency Injection
5. Ticket System Integration (Abstract)
6. Ticket System Implementation (OTOBO/Znuny)
7. Ticket System Pipes
8. Base Pipes
9. Template Rendering

**Interactive Layers:**
- `config_detail` - Detailed configuration structure
- `pipeline_execution` - Pipeline execution flow

**Rendering the D2 Diagram:**

Install D2:
```bash
# macOS
brew install d2

# Linux (download from https://github.com/terrastruct/d2/releases)
curl -fsSL https://d2lang.com/install.sh | sh -s --
```

Generate SVG:
```bash
d2 architecture_overview.d2 architecture_overview.svg
```

Generate with specific theme:
```bash
d2 --theme=200 architecture_overview.d2 architecture_overview.svg
```

Generate with specific layout:
```bash
d2 --layout=elk architecture_overview.d2 architecture_overview.svg
```

Interactive viewing with layers:
```bash
d2 --watch architecture_overview.d2
# Open browser to view and navigate layers
```

**References:**
- Related to issue [#353](https://github.com/Softoft-Orga/open-ticket-ai/issues/353) (PlantUML diagrams)
- Related to issue [#355](https://github.com/Softoft-Orga/open-ticket-ai/issues/355) (Mermaid diagrams)
- D2 Language Guide: `docs/_extra/d2/AI_README.md`

### Other Diagrams

- `otobo_demo_config_diagram.md` - OTOBO demo configuration diagram (Mermaid)
- `otobo_demo_pipeline_diagram.md` - OTOBO demo pipeline diagram (Mermaid)
- `pipeline_flow.md` - Pipeline flow diagram (Mermaid)
- `to_mermaid_conversion_simple.puml` - PlantUML to Mermaid conversion example

## Diagram Maintenance

When updating the architecture:

1. Update the D2 diagram (`architecture_overview.d2`) for multi-layered views
2. Update the PlantUML diagram (`architecture_overview.puml`) for traditional UML tools
3. Keep both diagrams synchronized for consistency
4. Follow the D2 best practices from `docs/_extra/d2/AI_README.md`
