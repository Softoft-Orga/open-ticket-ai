# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\context.py

from pydantic import BaseModel

from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.status import PipelineStatus


class PipelineContext[DataT: BaseModel](BaseModel):
    data: DataT = None
    meta_info: MetaInfo = MetaInfo()

    def stop_pipeline(self):
        self.meta_info.status = PipelineStatus.STOPPED
