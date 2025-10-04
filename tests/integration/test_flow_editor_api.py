"""Integration tests for the flow editor API endpoints.

These tests require FastAPI and its test client to be installed.
Run with: pytest tests/integration/test_flow_editor_api.py
"""

import tempfile
from pathlib import Path

try:
    import pytest
    from fastapi.testclient import TestClient
    
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    pytest = None  # type: ignore
    TestClient = None  # type: ignore


if DEPENDENCIES_AVAILABLE:
    from open_ticket_ai.tools.flow_editor_api.main import app
    from open_ticket_ai.tools.flow_editor_api.settings import Settings

    @pytest.fixture
    def temp_config_file():
        """Create a temporary config file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False, encoding='utf-8') as tmp:
            tmp.write("""
open_ticket_ai:
  defs:
    - id: test_pipeline
      steps:
        - id: step1
        - id: step2
          depends_on: [step1]
""")
            tmp_path = Path(tmp.name)
        
        yield tmp_path
        
        # Cleanup
        tmp_path.unlink(missing_ok=True)

    @pytest.fixture
    def client(temp_config_file, monkeypatch):
        """Create a test client with a temporary config file."""
        # Override the settings to use our temp config
        monkeypatch.setenv("CONFIG_PATH", str(temp_config_file))
        
        # Recreate the app with new settings
        from open_ticket_ai.tools.flow_editor_api import main as api_main
        api_main.settings = Settings()
        
        return TestClient(app)

    def test_health_check(client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_get_config(client):
        """Test getting the configuration."""
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert "yaml" in data
        assert "open_ticket_ai" in data["yaml"]

    def test_update_config(client, temp_config_file):
        """Test updating the configuration."""
        new_yaml = """
open_ticket_ai:
  defs:
    - id: updated_pipeline
      steps:
        - id: new_step
"""
        response = client.put("/config", json={"yaml": new_yaml})
        assert response.status_code == 200
        data = response.json()
        assert data["yaml"] == new_yaml
        
        # Verify the file was actually updated
        content = temp_config_file.read_text(encoding="utf-8")
        assert content == new_yaml

    def test_update_config_invalid_yaml(client):
        """Test updating config with invalid YAML."""
        invalid_yaml = "invalid: yaml: content: [unclosed"
        response = client.put("/config", json={"yaml": invalid_yaml})
        assert response.status_code == 400
        assert "Invalid YAML" in response.json()["detail"]

    def test_convert_without_yaml(client):
        """Test converting current config to Mermaid."""
        response = client.post("/convert", json={"direction": "TD", "wrap": False})
        assert response.status_code == 200
        data = response.json()
        assert "mermaid" in data
        assert "flowchart TD" in data["mermaid"]
        assert "test_pipeline" in data["mermaid"]

    def test_convert_with_inline_yaml(client):
        """Test converting inline YAML to Mermaid."""
        inline_yaml = """
open_ticket_ai:
  defs:
    - id: inline_test
      steps:
        - id: inline_step1
        - id: inline_step2
          depends_on: [inline_step1]
"""
        response = client.post("/convert", json={
            "yaml": inline_yaml,
            "direction": "TD",
            "wrap": False
        })
        assert response.status_code == 200
        data = response.json()
        assert "mermaid" in data
        assert "flowchart TD" in data["mermaid"]
        assert "inline_test" in data["mermaid"]

    def test_convert_with_lr_direction(client):
        """Test converting with LR direction."""
        response = client.post("/convert", json={"direction": "LR", "wrap": False})
        assert response.status_code == 200
        data = response.json()
        assert "flowchart LR" in data["mermaid"]

    def test_convert_invalid_direction(client):
        """Test converting with invalid direction."""
        response = client.post("/convert", json={"direction": "INVALID", "wrap": False})
        assert response.status_code == 400
        assert "Invalid direction" in response.json()["detail"]

    def test_cors_headers(client):
        """Test that CORS headers are set correctly."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            }
        )
        # CORS middleware should add these headers
        assert "access-control-allow-origin" in response.headers

else:
    # Dummy test that will be skipped when dependencies are not available
    def test_dependencies_not_available():
        """Skip tests if dependencies are not available."""
        import sys
        print("Skipping integration tests - FastAPI not installed", file=sys.stderr)
        assert True
