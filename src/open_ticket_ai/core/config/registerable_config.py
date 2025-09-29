import uuid

from pydantic import BaseModel, Field, ImportString


class RegisterableConfig(BaseModel):
    id: str = Field(default=uuid.uuid4().hex)
    use: ImportString = Field(
        default="open_ticket_ai.basic_pipes.DefaultPipe"
    )
