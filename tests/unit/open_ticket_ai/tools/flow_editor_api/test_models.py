"""Tests for the flow editor API models."""

from open_ticket_ai.tools.flow_editor_api.models import (
    ConfigResponse,
    ConfigUpdateRequest,
    ConvertRequest,
    ConvertResponse,
    HealthResponse,
)


def test_health_response():
    """Test HealthResponse model."""
    response = HealthResponse(status="ok")
    assert response.status == "ok"


def test_config_response():
    """Test ConfigResponse model."""
    yaml_content = "key: value"
    response = ConfigResponse(yaml=yaml_content)
    assert response.yaml == yaml_content


def test_config_update_request():
    """Test ConfigUpdateRequest model."""
    yaml_content = "key: new_value"
    request = ConfigUpdateRequest(yaml=yaml_content)
    assert request.yaml == yaml_content


def test_convert_request_defaults():
    """Test ConvertRequest model with default values."""
    request = ConvertRequest()
    assert request.yaml is None
    assert request.direction == "TD"
    assert request.wrap is False


def test_convert_request_with_values():
    """Test ConvertRequest model with custom values."""
    yaml_content = "key: value"
    request = ConvertRequest(yaml=yaml_content, direction="LR", wrap=True)
    assert request.yaml == yaml_content
    assert request.direction == "LR"
    assert request.wrap is True


def test_convert_response():
    """Test ConvertResponse model."""
    mermaid_content = "flowchart TD\n  A --> B"
    response = ConvertResponse(mermaid=mermaid_content)
    assert response.mermaid == mermaid_content
