# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\context.py
from collections import defaultdict
from typing import Any, Dict

from pydantic import BaseModel, Field


class PipeEvent(BaseModel):
    is_success: bool | None = None
    error_message: str | None = None
    error_name: str | None = None

class MetaInfo(BaseModel):
    events: Dict[str, Any] = Field(
        default_factory=lambda: defaultdict(dict),
        description="Nested dictionary for tracking pipeline events and their statuses",
    )


class PipelineContext(BaseModel):
    data: dict = {}
    meta_info: MetaInfo = MetaInfo()
    current_state: dict = {}
    pipeline_config: dict = {}
