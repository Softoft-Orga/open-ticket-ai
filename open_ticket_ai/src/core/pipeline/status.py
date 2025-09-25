# In a new or existing enums file, e.g., ce/run/pipeline/status.py
from enum import Enum, auto


class PipelineStatus(Enum):
    RUNNING = auto()
    SUCCESS = auto()
    STOPPED = auto()
    PARTIAL_FAILURE = auto()
    FAILED = auto()

