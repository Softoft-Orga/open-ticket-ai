from typing import Any

from pydantic import BaseModel


class Context(BaseModel):
    pipes: dict[str, dict[str, Any]] = {}
    config: dict[str, Any] = {}
