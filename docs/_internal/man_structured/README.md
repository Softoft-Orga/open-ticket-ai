# Sidecar Documentation Structure

This directory contains structured sidecar YAML files for all Pipes, Services, and Triggers in Open Ticket AI. These sidecars provide comprehensive metadata, configuration details, usage examples, and error information for documentation and UI components.

## Directory Structure

```
docs/_internal/man_structured/
├── README.md                    # This file
├── pipes/                       # Sidecar files for Pipe components
│   ├── *.sidecar.yml           # Individual pipe sidecars
│   └── sidecar_pipe_schema.yml # Schema/template for pipe sidecars
├── services/                    # Sidecar files for Service components
│   └── *.sidecar.yml           # Individual service sidecars
└── triggers/                    # Sidecar files for Trigger components
    └── *.sidecar.yml           # Individual trigger sidecars
```

## Sidecar File Naming Convention

Sidecar files follow a consistent naming pattern:

- **Format**: `{component_name}.sidecar.yml`
- **Example**: `add_note_pipe.sidecar.yml`, `interval_trigger.sidecar.yml`
- Component names should be in snake_case
- The `.sidecar.yml` suffix clearly identifies the file type

## Sidecar Structure

All sidecars follow a consistent YAML structure with the following top-level fields:

### Required Fields

- **`_version`**: Version of the sidecar format (e.g., `1.0.x`)
- **`_class`**: Fully qualified Python class name (e.g., `open_ticket_ai.base.CompositePipe`)
- **`_extends`**: Parent class that this component extends
- **`_title`**: Human-readable title for the component
- **`_summary`**: Brief description of what the component does
- **`_category`**: Component category (e.g., `ticket-system`, `ml-classification`, `orchestration`)

### Input Configuration

- **`_inputs`**: Describes how the component accepts parameters
  - `placement`: Where parameters are placed (`flat`, `services`, etc.)
  - `alongside`: Fields that appear alongside the component (e.g., `[id, use]`)
  - `params`: Dictionary of parameter names and their descriptions

### Defaults and Output

- **`_defaults`**: Default values for parameters (can be empty `{}`)
- **`_output`**: Describes component output
  - `state_enum`: Possible output states (e.g., `[ok, skipped, failed]`)
  - `description`: Description of the output behavior
  - `payload_schema_ref`: Reference to the payload schema
  - `examples`: Example outputs for each state

### Error Handling

- **`_errors`**: Categorized error definitions
  - `fail`: Errors that cause the component to fail
  - `break`: Critical errors that stop execution
  - `continue`: Non-critical errors that allow continuation
  - Each error has:
    - `code`: Unique error identifier
    - `when`: Description of when this error occurs

### Engine Support

- **`_engine_support`**: Feature flags for engine capabilities
  - `on_failure`: Whether the component supports failure hooks
  - `on_success`: Whether the component supports success hooks

### Usage Examples

- **`_examples`**: Practical usage examples in YAML format
  - `minimal`: Simplest possible usage
  - `full`: Complete usage with common options
  - `large`: Complex real-world usage example

## Component Categories

### Pipes

Located in `pipes/`, these transform data and perform actions:

- **ticket-system**: Interact with ticket systems (AddNote, FetchTickets, UpdateTicket)
- **ml-classification**: Machine learning classification tasks
- **orchestration**: Workflow composition (CompositePipe)
- **utility**: Helper operations (JinjaExpression)

### Services

Located in `services/`, these provide external system integrations:

- **ticket-system**: Ticket system service adapters (OTOBO/Znuny)

### Triggers

Located in `triggers/`, these define when pipelines execute:

- **scheduling**: Time-based triggers (IntervalTrigger)

## Adding a New Sidecar

When adding a new Pipe, Service, or Trigger to the codebase:

1. **Create the sidecar file** in the appropriate directory
2. **Follow the naming convention**: `{component_name}.sidecar.yml`
3. **Use existing sidecars as templates** - refer to `add_note_pipe.sidecar.yml` for pipes
4. **Validate the structure** - ensure all required fields are present
5. **Provide comprehensive examples** - minimal, full, and large usage scenarios
6. **Document all errors** - categorize as fail/break/continue appropriately
7. **Keep descriptions clear** - use concise, actionable language

## Validation

To validate that all components have sidecars, run:

```bash
uv run python scripts/validate_sidecars.py
```

This script will:
- Scan the codebase for all Pipe, Service, and Trigger classes
- Check that each has a corresponding sidecar file
- Validate the sidecar structure against the schema
- Report any missing or invalid sidecars

## Building the Sidecars Index

The sidecars are compiled into a JSON index file for runtime consumption by the documentation site:

```bash
python3 scripts/build_sidecars_json.py
```

This generates `docs/public/assets/sidecars.json` containing all sidecar data organized by type and name.

**Note**: This file is automatically generated during the documentation build process (`npm run docs:build`) and should not be committed to the repository.

## Integration with Documentation

These sidecars are consumed by:

1. **VitePress Documentation**: The `PipeSidecar.vue` component renders sidecars in the documentation
2. **Composable**: `useSidecars.ts` loads and provides access to all sidecars
3. **Build Process**: A build script generates `sidecars.json` for runtime access

### Loading Sidecars in Vue Components

```typescript
import { useSidecars } from '@/.vitepress/composables/useSidecars'

const { getSidecar, filterByType, filterByCategory } = useSidecars()

// Get a specific sidecar
const addNotePipe = getSidecar('pipe', 'add_note_pipe')

// Filter by type
const allPipes = filterByType('pipe')
const allServices = filterByType('service')
const allTriggers = filterByType('trigger')

// Filter by category
const ticketSystemPipes = filterByCategory('ticket-system')
```

## Maintenance

### Updating Existing Sidecars

When updating a component:

1. Update the corresponding sidecar to reflect changes
2. Ensure examples are still valid and accurate
3. Add new parameters to `_inputs.params`
4. Update error codes if error handling changes
5. Increment `_version` if the sidecar format changes

### Moving or Renaming Components

If a component is moved or renamed:

1. Update the `_class` field with the new fully qualified name
2. Rename the sidecar file to match the new component name
3. Update any references in the documentation

## Schema Reference

For detailed information about the sidecar schema, see:

- `pipes/sidecar_pipe_schema.yml` - Schema for pipe sidecars
- `docs/.vitepress/components/pipe/pipeSidecar.types.ts` - TypeScript interface definitions

## Current Inventory

### Pipes (6 component files + 2 templates)
**Component Sidecars:**
- `add_note_pipe.sidecar.yml` - Adds notes to tickets
- `composite_pipe.sidecar.yml` - Orchestrates multiple steps
- `fetch_tickets_pipe.sidecar.yml` - Retrieves tickets from systems
- `hf_local_text_classification_pipe.sidecar.yml` - HuggingFace text classification
- `jinja_expression_pipe.sidecar.yml` - Evaluates Jinja expressions
- `update_ticket_pipe.sidecar.yml` - Updates ticket properties

**Templates/Reference:**
- `default_pipe.sidecar.yml` - Template/example for no-op placeholder pipes
- `sidecar_pipe_schema.yml` - Schema reference with multilingual support example

### Services (1 file)
- `otobo_znuny_ticket_system_service.sidecar.yml` - OTOBO/Znuny integration

### Triggers (1 file)
- `interval_trigger.sidecar.yml` - Time-based trigger

---

**Last Updated**: 2025-10-13  
**Maintainer**: Open Ticket AI Documentation Team
