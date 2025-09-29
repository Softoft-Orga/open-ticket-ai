import uuid
from typing import Any

from pydantic import BaseModel, Field, ImportString


class RegisterableConfig(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    name: str = Field(default="")
    use: ImportString = Field(
        default="open_ticket_ai.basic_pipes.DefaultPipe"
    )
    when: bool = Field(default=True)
    steps: list[dict[str, Any]] = Field(default_factory=list)
