from __future__ import annotations

from typing import Literal

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingConfig(StrictBaseModel):
    level: LogLevel = Field(
        default="INFO",
        description=(
            "The minimum severity level of log messages to record, "
            "ranging from DEBUG (most verbose) to CRITICAL (least verbose)."
        ),
    )
    log_to_file: bool = Field(
        default=False,
        description="Whether to write log messages to a file in addition to or instead of console output.",
    )
    log_file_path: str | None = Field(
        default=None, description="File system path where log messages should be written when log_to_file is enabled."
    )
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Format string for log messages following Python's logging format specification.",
    )
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Format string for timestamp in log messages following Python's strftime format specification.",
    )
