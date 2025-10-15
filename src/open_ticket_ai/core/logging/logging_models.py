from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingConfig(BaseModel):
    level: LogLevel = "INFO"
    log_to_file: bool = False
    log_file_path: str | None = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
