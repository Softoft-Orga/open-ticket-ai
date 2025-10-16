from pydantic import BaseModel, ConfigDict


class OpenTicketAIBaseModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


StrictBaseModel = OpenTicketAIBaseModel
