from packages.api.models import (
    ConfigResponse,
    ConfigUpdateRequest,
    ConvertRequest,
    ConvertResponse,
    HealthResponse,
)


def test_health_response():
    response = HealthResponse(status="ok")
    assert response.status == "ok"


def test_config_response():
    yaml_content = "key: value"
    response = ConfigResponse(yaml=yaml_content)
    assert response.yaml == yaml_content


def test_config_update_request():
    yaml_content = "key: new_value"
    request = ConfigUpdateRequest(yaml=yaml_content)
    assert request.yaml == yaml_content


def test_convert_request_defaults():
    request = ConvertRequest()
    assert request.yaml is None
    assert request.direction == "TD"
    assert request.wrap is False


def test_convert_request_with_values():
    yaml_content = "key: value"
    request = ConvertRequest(yaml=yaml_content, direction="LR", wrap=True)
    assert request.yaml == yaml_content
    assert request.direction == "LR"
    assert request.wrap is True


def test_convert_response():
    mermaid_content = "flowchart TD\n  A --> B"
    response = ConvertResponse(mermaid=mermaid_content)
    assert response.mermaid == mermaid_content
