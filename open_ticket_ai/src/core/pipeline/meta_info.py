from pydantic import BaseModel

from open_ticket_ai.src.core.pipeline.status import PipelineStatus


class MetaInfo(BaseModel):
    status: PipelineStatus = PipelineStatus.RUNNING
    error_message: str | None = None
    failed_pipe: str | None = None
