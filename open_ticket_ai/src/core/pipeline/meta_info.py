from typing import Optional

from pydantic import BaseModel

from open_ticket_ai.src.core.pipeline.status import PipelineStatus


class MetaInfo(BaseModel):
    status: PipelineStatus = PipelineStatus.RUNNING
    error_message: Optional[str] = None
    failed_pipe: Optional[str] = None
