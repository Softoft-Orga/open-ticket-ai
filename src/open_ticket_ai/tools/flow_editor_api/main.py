"""FastAPI application for the flow editor API."""

from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
except ImportError as exc:
    raise ImportError(
        "FastAPI is required to run the flow editor API. "
        "Install it with: pip install fastapi uvicorn"
    ) from exc

from .models import (
    ConfigResponse,
    ConfigUpdateRequest,
    ConvertRequest,
    ConvertResponse,
    HealthResponse,
)
from .service import convert_yaml_to_mermaid, load_config_yaml, save_config_yaml
from .settings import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Open Ticket AI Flow Editor API",
    description="REST API for otai-flow-editor integration",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse with status "ok"
    """
    return HealthResponse(status="ok")


@app.get("/config", response_model=ConfigResponse)
async def get_config() -> ConfigResponse:
    """Get current configuration.

    Returns:
        ConfigResponse containing current YAML configuration

    Raises:
        HTTPException: 404 if config file not found, 500 for other errors
    """
    try:
        yaml_content = load_config_yaml(settings.config_path)
        return ConfigResponse(yaml=yaml_content)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration file not found: {settings.config_path}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading configuration: {str(exc)}",
        ) from exc


@app.put("/config", response_model=ConfigResponse)
async def update_config(request: ConfigUpdateRequest) -> ConfigResponse:
    """Update configuration.

    Args:
        request: ConfigUpdateRequest with new YAML content

    Returns:
        ConfigResponse with the updated configuration

    Raises:
        HTTPException: 400 for invalid YAML, 500 for write errors
    """
    try:
        # Validate YAML by trying to parse it
        import yaml
        try:
            yaml.safe_load(request.yaml)
        except yaml.YAMLError as yaml_exc:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid YAML: {str(yaml_exc)}",
            ) from yaml_exc
        
        # Save the configuration
        save_config_yaml(settings.config_path, request.yaml)
        
        return ConfigResponse(yaml=request.yaml)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error writing configuration: {str(exc)}",
        ) from exc


@app.post("/convert", response_model=ConvertResponse)
async def convert_to_mermaid(request: ConvertRequest) -> ConvertResponse:
    """Convert YAML configuration to Mermaid diagram.

    Args:
        request: ConvertRequest with optional YAML, direction, and wrap settings

    Returns:
        ConvertResponse with generated Mermaid diagram

    Raises:
        HTTPException: 400 for invalid input, 500 for conversion errors
    """
    try:
        # Validate direction
        if request.direction not in ["TD", "LR"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid direction. Must be 'TD' or 'LR'",
            )
        
        # Convert to Mermaid
        mermaid_content = convert_yaml_to_mermaid(
            yaml_content=request.yaml,
            config_path=settings.config_path,
            direction=request.direction,
            wrap=request.wrap,
        )
        
        return ConvertResponse(mermaid=mermaid_content)
    except HTTPException:
        raise
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration file not found: {settings.config_path}",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid configuration: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting to Mermaid: {str(exc)}",
        ) from exc


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
