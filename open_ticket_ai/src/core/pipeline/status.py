# In a new or existing enums file, e.g., ce/run/pipeline/status.py
from enum import Enum, auto


class PipelineStatus(Enum):
    """Represents the possible states of a pipeline execution.

    This enum defines the various statuses a pipeline can have during its lifecycle.

    Attributes:
        RUNNING: Indicates the pipeline is currently executing.
        SUCCESS: Indicates the pipeline completed successfully without errors.
        STOPPED: Indicates the pipeline was intentionally halted (controlled stop).
        FAILED: Indicates the pipeline terminated due to an unexpected error.
    """

    RUNNING = auto()
    SUCCESS = auto()
    STOPPED = auto()
    FAILED = auto()
