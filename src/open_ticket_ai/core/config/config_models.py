from __future__ import annotations

from packaging.specifiers import SpecifierSet
from pydantic import BaseModel, Field, field_validator

from open_ticket_ai.core.config.types import VersionSpecifier
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig, InjectableConfigBase
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


class InfrastructureConfig(BaseModel):
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig,
        description="Configuration for application logging including level, format, and output destination.",
    )


class PluginConfig(BaseModel):
    name: str = Field(
        default="",
        description="Name of the plugin for identification purposes.",
    )
    version: VersionSpecifier = Field(
        default=">=0.0.0",
        description="Version of the plugin for compatibility management.",
    )


class OpenTicketAIConfig(BaseModel):
    api_version: VersionSpecifier = Field(  # type: ignore[assignment]
        default=">=1.0.0",
        description="API version of the OpenTicketAI application for compatibility and feature management.",
    )
    plugins: list[PluginConfig] = Field(
        default_factory=list,
        description="List of plugin module paths to load and enable for extending application functionality.",
    )
    infrastructure: InfrastructureConfig = Field(
        default_factory=InfrastructureConfig,
        description="Infrastructure-level configuration including logging and template rendering settings.",
    )
    services: dict[str, InjectableConfigBase] = Field(
        default_factory=dict,
        description="List of service configurations defining available ticket system integrations and other services.",
    )
    orchestrator: PipeConfig = Field(
        default_factory=PipeConfig,
        description="Orchestrator configuration defining runners, triggers, and pipes execution workflow.",
    )

    def get_services_list(self) -> list[InjectableConfig]:
        return [
            InjectableConfig.model_validate({"id": _id, **service_base.model_dump()})
            for _id, service_base in self.services.items()
        ]

    @field_validator("api_version")
    @classmethod
    def validate_spec(cls, v: str) -> str:
        """Ensure the version spec is valid."""
        try:
            SpecifierSet(v)
        except Exception as e:
            raise ValueError(f"Invalid version specifier '{v}': {e}") from e
        return v
