# Flow Editor API - Quick Start Guide

## For Vue Frontend Developers

### API Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

#### 2. Get Configuration
```http
GET /config
```

Response:
```json
{
  "yaml": "open_ticket_ai:\n  defs: [...]\n  orchestrator: [...]"
}
```

#### 3. Update Configuration
```http
PUT /config
Content-Type: application/json

{
  "yaml": "open_ticket_ai:\n  defs: [...]\n  orchestrator: [...]"
}
```

Response:
```json
{
  "yaml": "open_ticket_ai:\n  defs: [...]\n  orchestrator: [...]"
}
```

#### 4. Convert to Mermaid Diagram
```http
POST /convert
Content-Type: application/json

{
  "yaml": "open_ticket_ai:\n  defs: [...]",  // Optional
  "direction": "TD",                           // "TD" or "LR"
  "wrap": false                                // Boolean
}
```

Response:
```json
{
  "mermaid": "flowchart TD\n  A --> B\n  ..."
}
```

### CORS Configuration

The API is pre-configured to accept requests from:
- `http://localhost:5173` (Vue dev server default port)

### Example JavaScript/TypeScript Usage

```typescript
// Health check
const health = await fetch('http://localhost:8000/health');
const healthData = await health.json();
console.log(healthData.status); // "ok"

// Get config
const config = await fetch('http://localhost:8000/config');
const configData = await config.json();
console.log(configData.yaml);

// Update config
const updateResponse = await fetch('http://localhost:8000/config', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ yaml: newYamlContent })
});
const updatedConfig = await updateResponse.json();

// Convert to Mermaid (using current config)
const convertResponse = await fetch('http://localhost:8000/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ direction: 'TD', wrap: false })
});
const mermaidData = await convertResponse.json();
console.log(mermaidData.mermaid);

// Convert to Mermaid (with inline YAML)
const convertInlineResponse = await fetch('http://localhost:8000/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    yaml: yamlContent,
    direction: 'LR',
    wrap: false
  })
});
const mermaidInlineData = await convertInlineResponse.json();
```

## For Backend Developers

### Starting the API

**Development:**
```bash
python examples/run_flow_editor_api.py
```

Or:
```bash
python -m open_ticket_ai.tools.flow_editor_api.main
```

Or with uvicorn:
```bash
uvicorn open_ticket_ai.tools.flow_editor_api.main:app --reload --host 0.0.0.0 --port 8000
```

**Production:**
```bash
uvicorn open_ticket_ai.tools.flow_editor_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables

- `CONFIG_PATH`: Path to config.yml (default: `src/config.yml`)

Example:
```bash
export CONFIG_PATH=/path/to/custom/config.yml
python examples/run_flow_editor_api.py
```

### Running Tests

```bash
# Unit tests (no external dependencies required)
pytest tests/unit/open_ticket_ai/tools/flow_editor_api/

# Integration tests (requires FastAPI)
pytest tests/integration/test_flow_editor_api.py
```

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Architecture Overview

```
src/open_ticket_ai/tools/flow_editor_api/
├── __init__.py       # Package initialization
├── main.py           # FastAPI app and endpoints
├── models.py         # Pydantic request/response models
├── settings.py       # Configuration management
├── storage.py        # File I/O operations
├── service.py        # Business logic
└── README.md         # Detailed documentation
```

### Dependencies

- FastAPI >= 0.115.0
- Uvicorn >= 0.32.0
- Pydantic ~= 2.11.7
- pydantic-settings >= 2.0.0
- PyYAML >= 6.0.2

Install with:
```bash
pip install fastapi uvicorn pydantic pydantic-settings pyyaml
```

Or install the full project:
```bash
pip install -e .
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors:
1. Check that the Vue dev server is running on `http://localhost:5173`
2. If using a different port, update `cors_origins` in `settings.py`
3. Restart the API server after making changes

### Config File Not Found

If you get a 404 error on `/config`:
1. Ensure the config file exists at the path specified by `CONFIG_PATH`
2. Default path is `src/config.yml` relative to the project root
3. Set `CONFIG_PATH` environment variable to point to your config file

### Invalid YAML

If you get a 400 error when updating config:
1. Validate your YAML syntax using an online validator
2. Ensure proper indentation (2 spaces, not tabs)
3. Check for missing colons or quotes

## Support

For issues or questions:
- Check the main README: `src/open_ticket_ai/tools/flow_editor_api/README.md`
- Review the test files for usage examples
- Open an issue on GitHub
