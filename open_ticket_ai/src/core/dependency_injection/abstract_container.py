import abc

from open_ticket_ai.src.core.mixins.registry_providable_instance import (
    Providable,
)
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class AbstractContainer(abc.ABC):
    @abc.abstractmethod
    def get_instance[T: Providable](self, provider_key: str,
                                    subclass_of: type[T]) -> T:
        pass

    @abc.abstractmethod
    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        pass
