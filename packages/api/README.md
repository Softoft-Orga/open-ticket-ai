# Flow Editor API

Minimal FastAPI REST API for otai-flow-editor Vue app.

## Installation

Install dependencies:

```bash
pip install -e .
```

## Configuration

Set CONFIG_PATH env variable for config file location.

## Running

Development:

```bash
python -m open_ticket_ai.tools.flow_editor_api.main
```

Production:

```bash
uvicorn open_ticket_ai.tools.flow_editor_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Endpoints

- GET /health: Health check
- GET /config: Get config YAML
- PUT /config: Update config
- POST /convert: Convert YAML to Mermaid diagram

## CORS

Default: http://localhost:5173

## Architecture

- models.py: Pydantic models
- settings.py: Config management
- storage.py: YAML file I/O
- service.py: YAML to Mermaid logic
- main.py: FastAPI app

## Mermaid Conversion

Uses ConfigFlowDiagramGenerator and MermaidDiagramRenderer from open_ticket_ai.diagram.

## Testing

Run tests:

```bash
pytest tests/unit/open_ticket_ai/tools/flow_editor_api/
```

## License

LGPL-2.1
