import abc

from open_ticket_ai.src.core.mixins.registry_providable_instance import (
    Providable,
)
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline


class AbstractContainer(abc.ABC):
    """Abstract interface for dependency containers.

    This class defines the contract for dependency injection containers that manage
    object instances. Implementations should provide mechanisms to register and
    retrieve instances based on provider keys and type constraints.

    The container acts as a central registry that decouples object creation and
    dependencies from their usage, enabling more modular and testable code.
    """

    @abc.abstractmethod
    def get_instance[T: Providable](self, provider_key: str,
                                    subclass_of: type[T]) -> T:
        """Retrieve an instance from the container.

        The instance is retrieved based on the provider key and must be a subclass of the given type.

        Args:
            provider_key: The key identifying the provider for the instance.
            subclass_of: The class (or type) of the instance to be retrieved. The type T must be a subclass of
                `Providable`.

        Returns:
            An instance of the type specified by `subclass_of`.

        Raises:
            InstanceNotFoundError: If no instance matching the provider key is found.
            TypeMismatchError: If the found instance is not a subclass of the specified type.
        """
        pass

    @abc.abstractmethod
    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        pass
