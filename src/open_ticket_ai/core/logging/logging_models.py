from __future__ import annotations

from typing import Literal

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingFormatConfig(StrictBaseModel):
    message_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Python logging format string",
    )
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Python strftime format for timestamps",
    )


class LoggingConfig(StrictBaseModel):
    level: LogLevel = Field(
        default="INFO",
        description="Minimum severity level",
    )
    log_to_file: bool = Field(
        default=False,
        description="Write logs to a file",
    )
    log_file_path: str | None = Field(
        default=None,
        description="Path for file logs when enabled",
    )
    format: LoggingFormatConfig = Field(
        default_factory=LoggingFormatConfig,
        description="Message and date formats",
    )
