import abc

from open_ticket_ai.src.core.mixins.registry_providable_instance import (
    Providable,
)
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class AbstractContainer(abc.ABC):
    @abc.abstractmethod
    def get_pipe(self, provider_key: str) -> Pipe:
        pass

    @abc.abstractmethod
    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        pass
