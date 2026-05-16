from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
TicketSystemType = Literal["otobo", "zammad"]


# ── Ticket-system settings (source-agnostic: env vars, Studio UI, …) ──


class OtoboTicketSystemSettings(BaseModel):
    type: Literal["otobo"] = "otobo"
    base_url: str = Field(
        default="http://localhost/otobo/nph-genericinterface.pl",
        description="Base URL of the OTOBO/Znuny generic-interface endpoint",
    )
    username: str = Field(default="open_ticket_ai")
    password: str = Field(default="")
    webservice_name: str = Field(default="OpenTicketAI")


class ZammadTicketSystemSettings(BaseModel):
    type: Literal["zammad"] = "zammad"
    base_url: str = Field(description="Base URL of the Zammad instance")
    access_token: str = Field(description="Personal access token for the Zammad API")


TicketSystemSettings = Annotated[
    OtoboTicketSystemSettings | ZammadTicketSystemSettings,
    Field(discriminator="type"),
]


# ── Runtime settings (env-var / .env driven) ─────────────────────────


OPERATIONAL = {"restart_required": False, "category": "operational"}
INFRASTRUCTURE = {"restart_required": True, "category": "infrastructure"}
SECRET_INFRASTRUCTURE = {"restart_required": True, "category": "infrastructure", "secret": True}


class Settings(BaseSettings):
    """Flat env-var / .env driven settings for Open Ticket AI runtime."""

    model_config = SettingsConfigDict(
        env_prefix="OTAI_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    log_level: LogLevel = Field(
        default="INFO",
        description="Log verbosity level",
        json_schema_extra=OPERATIONAL,
    )

    # API server
    api_host: str = Field(  # noqa: S104
        default="0.0.0.0",
        description="Host to bind the API server",
        json_schema_extra=INFRASTRUCTURE,
    )
    api_port: int = Field(
        default=8080,
        description="Port to bind the API server",
        json_schema_extra=INFRASTRUCTURE,
    )

    # Ticket system selection (flat env vars, bridged via .ticket_system)
    ticket_system_type: TicketSystemType = Field(
        default="otobo",
        description="Which ticket system backend to use",
        json_schema_extra=INFRASTRUCTURE,
    )
    otobo_base_url: str = Field(
        default="http://localhost/otobo/nph-genericinterface.pl",
        description="Base URL of the OTOBO/Znuny instance",
        json_schema_extra=INFRASTRUCTURE,
    )
    otobo_username: str = Field(
        default="open_ticket_ai",
        description="OTOBO/Znuny API username",
        json_schema_extra=SECRET_INFRASTRUCTURE,
    )
    otobo_password: str = Field(
        default="",
        description="OTOBO/Znuny API password",
        json_schema_extra=SECRET_INFRASTRUCTURE,
    )
    otobo_webservice_name: str = Field(
        default="OpenTicketAI",
        description="OTOBO/Znuny web service name",
        json_schema_extra=INFRASTRUCTURE,
    )
    zammad_base_url: str | None = Field(
        default=None,
        description="Base URL of the Zammad instance",
        json_schema_extra=INFRASTRUCTURE,
    )
    zammad_access_token: str | None = Field(
        default=None,
        description="Personal access token for the Zammad API",
        json_schema_extra=SECRET_INFRASTRUCTURE,
    )

    # HuggingFace
    hf_api_token: str | None = Field(
        default=None,
        description="HuggingFace API token for model access",
        json_schema_extra=SECRET_INFRASTRUCTURE,
    )

    # Pipeline tuning
    orchestrator_sleep: float = Field(
        default=0.01,
        description="Seconds between orchestration cycles",
        json_schema_extra=OPERATIONAL,
    )
    trigger_interval: float = Field(
        default=0.1,
        description="Seconds between trigger checks",
        json_schema_extra=OPERATIONAL,
    )
    classification_confidence_threshold: float = Field(
        default=0.8,
        description="Minimum confidence to accept a classification (0-1)",
        json_schema_extra=OPERATIONAL,
    )

    # Queue / model config
    incoming_queue: str = Field(
        default="OpenTicketAI::Incoming",
        description="Queue to poll for new tickets",
        json_schema_extra=OPERATIONAL,
    )
    fallback_queue: str = Field(
        default="OpenTicketAI::Unclassified",
        description="Queue assigned when confidence is below threshold",
        json_schema_extra=OPERATIONAL,
    )
    fallback_priority: str = Field(
        default="medium",
        description="Priority assigned when confidence is below threshold",
        json_schema_extra=OPERATIONAL,
    )
    queue_model: str = Field(
        default="softoft/otai-queue-de-bert-v1",
        description="HuggingFace model for queue classification",
        json_schema_extra=OPERATIONAL,
    )
    priority_model: str = Field(
        default="softoft/otai-priority-de-bert-v1",
        description="HuggingFace model for priority classification",
        json_schema_extra=OPERATIONAL,
    )

    @property
    def ticket_system(self) -> OtoboTicketSystemSettings | ZammadTicketSystemSettings:
        """Bridge flat env vars into a self-contained TicketSystemSettings."""
        if self.ticket_system_type == "zammad":
            if not self.zammad_base_url or not self.zammad_access_token:
                msg = "OTAI_ZAMMAD_BASE_URL and OTAI_ZAMMAD_ACCESS_TOKEN are required when ticket_system_type=zammad"
                raise ValueError(msg)
            return ZammadTicketSystemSettings(
                base_url=self.zammad_base_url,
                access_token=self.zammad_access_token,
            )
        return OtoboTicketSystemSettings(
            base_url=self.otobo_base_url,
            username=self.otobo_username,
            password=self.otobo_password,
            webservice_name=self.otobo_webservice_name,
        )
