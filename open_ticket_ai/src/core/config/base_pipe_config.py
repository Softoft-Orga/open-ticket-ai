from pydantic import BaseModel, Field


class BasePipeConfig(BaseModel):
    class_path: str = Field(..., description="Dotted path to the Pipe class")
    when: str = "true"
