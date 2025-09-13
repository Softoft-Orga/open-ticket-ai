# FILE_PATH: open_ticket_ai\src\ce\run\pipeline\context.py

from pydantic import BaseModel

from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.status import PipelineStatus


class PipelineContext[DataT: BaseModel](BaseModel):
    """Context object passed between pipeline stages.

    This generic class serves as a container for sharing state and data across
    different stages of a processing pipeline. It leverages Pydantic for data
    validation and serialization.

    The generic type parameter `DataT` must be a subclass of `BaseModel`,
    ensuring type safety for the main data payload.

    Attributes:
        data (DataT): The main data payload being processed through the pipeline.
            Must be a Pydantic model instance matching the generic type.
        meta_info (MetaInfo): Metadata about the pipeline execution, including
            status information and operational details.
    """

    data: DataT = None
    meta_info: MetaInfo = MetaInfo()

    def stop_pipeline(self):
        """Signals the pipeline to halt processing.

        This method provides a controlled way for pipeline stages to indicate
        that processing should stop. It updates the context's status metadata
        to `STOPPED`, which subsequent stages can check to terminate early.

        Note:
            This method modifies the context's state but does not return any value.
        """
        self.meta_info.status = PipelineStatus.STOPPED
