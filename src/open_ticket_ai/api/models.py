"""Pydantic models for the flow editor API."""

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Health status of the API")


class ConfigResponse(BaseModel):
    """Response model for GET /config endpoint."""

    yaml: str = Field(..., description="Current configuration as YAML string")


class ConfigUpdateRequest(BaseModel):
    """Request model for PUT /config endpoint."""

    yaml: str = Field(..., description="New configuration as YAML string")


class ConvertRequest(BaseModel):
    """Request model for POST /convert endpoint."""

    yaml: Optional[str] = Field(None, description="Optional YAML configuration to convert")
    direction: str = Field("TD", description="Mermaid diagram direction (TD or LR)")
    wrap: bool = Field(False, description="Whether to wrap long labels")


class ConvertResponse(BaseModel):
    """Response model for POST /convert endpoint."""

    mermaid: str = Field(..., description="Generated Mermaid diagram")
