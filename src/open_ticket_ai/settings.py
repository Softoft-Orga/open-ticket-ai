from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Flat env-var / .env driven settings for Open Ticket AI runtime."""

    model_config = SettingsConfigDict(
        env_prefix="OTAI_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    log_level: LogLevel = Field(default="INFO")

    # OTOBO / Znuny ticket system
    otobo_base_url: str = Field(
        default="http://localhost/otobo/nph-genericinterface.pl",
        description="Base URL of the OTOBO/Znuny instance",
    )
    otobo_username: str = Field(default="open_ticket_ai")
    otobo_password: str = Field(default="")
    otobo_webservice_name: str = Field(default="OpenTicketAI")

    # HuggingFace
    hf_api_token: str | None = Field(default=None)

    # Zammad (optional)
    zammad_base_url: str | None = Field(default=None)
    zammad_access_token: str | None = Field(default=None)

    # Pipeline tuning
    orchestrator_sleep: float = Field(default=0.01, description="Seconds between orchestration cycles")
    trigger_interval: float = Field(default=0.1, description="Seconds between trigger checks")
    classification_confidence_threshold: float = Field(default=0.8)

    # Queue / model config
    incoming_queue: str = Field(default="OpenTicketAI::Incoming")
    fallback_queue: str = Field(default="OpenTicketAI::Unclassified")
    fallback_priority: str = Field(default="medium")
    queue_model: str = Field(default="softoft/otai-queue-de-bert-v1")
    priority_model: str = Field(default="softoft/otai-priority-de-bert-v1")
