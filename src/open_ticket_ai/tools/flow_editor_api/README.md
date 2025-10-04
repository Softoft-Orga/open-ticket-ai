# Flow Editor API

A minimal, production-ready FastAPI REST API for the otai-flow-editor Vue web application.

## Overview

This API provides endpoints for managing Open Ticket AI configuration files and converting them to Mermaid diagrams for visualization in the flow editor.

## Installation

The API requires the following dependencies:

```bash
pip install fastapi uvicorn pydantic pydantic-settings pyyaml
```

Or install the full project:

```bash
pip install -e .
```

## Configuration

The API can be configured via environment variables:

- `CONFIG_PATH`: Path to the config.yml file (default: `src/config.yml`)

Example:
```bash
export CONFIG_PATH=/path/to/your/config.yml
```

## Running the API

### Development Server

```bash
python -m open_ticket_ai.tools.flow_editor_api.main
```

Or using uvicorn directly:

```bash
uvicorn open_ticket_ai.tools.flow_editor_api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn open_ticket_ai.tools.flow_editor_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /config

Get the current configuration as YAML.

**Response:**
```json
{
  "yaml": "<yaml content>"
}
```

### PUT /config

Update the configuration.

**Request:**
```json
{
  "yaml": "<yaml content>"
}
```

**Response:**
```json
{
  "yaml": "<yaml content>"
}
```

### POST /convert

Convert YAML configuration to Mermaid diagram.

**Request:**
```json
{
  "yaml": "<yaml content>",  // Optional, uses current config if not provided
  "direction": "TD",          // TD (top-down) or LR (left-right)
  "wrap": false               // Whether to wrap long labels
}
```

**Response:**
```json
{
  "mermaid": "<mermaid diagram>"
}
```

## CORS

The API is configured to allow requests from:
- `http://localhost:5173` (Vue dev server)

To add additional origins, modify the `cors_origins` setting in `settings.py`.

## Architecture

The API is structured into several modules:

- **`models.py`**: Pydantic models for request/response validation
- **`settings.py`**: Configuration management using pydantic-settings
- **`storage.py`**: File I/O helpers for reading/writing YAML files
- **`service.py`**: Business logic for YAML conversion to Mermaid diagrams
- **`main.py`**: FastAPI application with endpoint definitions

## Integration with Mermaid Conversion

The API integrates with the existing diagram generation code from `open_ticket_ai.diagram`:

- `ConfigFlowDiagramGenerator`: Loads configuration and generates diagrams
- `MermaidDiagramRenderer`: Renders pipeline diagrams as Mermaid flowcharts

## Testing

Run the test suite:

```bash
pytest tests/unit/open_ticket_ai/tools/flow_editor_api/
```

## Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Get current config
curl http://localhost:8000/config

# Update config
curl -X PUT http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"yaml": "open_ticket_ai:\n  defs: []"}'

# Convert to Mermaid (using current config)
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"direction": "TD", "wrap": false}'

# Convert to Mermaid (with inline YAML)
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"yaml": "open_ticket_ai:\n  defs:\n    - id: test\n      steps:\n        - id: step1", "direction": "LR"}'
```

## Requirements

- Python 3.13+
- FastAPI >= 0.115.0
- Uvicorn >= 0.32.0
- Pydantic ~= 2.11.7
- pydantic-settings >= 2.0.0
- PyYAML >= 6.0.2

## License

This code is part of the Open Ticket AI project and is licensed under LGPL-2.1.
