import logging
from collections.abc import Iterable

from open_ticket_ai.core.config.errors import InjectableNotFoundError, RegistryError
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.pipes.pipe import Pipe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComponentRegistry:
    def __init__(self) -> None:
        self._injectables: dict[str, type[Injectable]] = {}

    def register(self, registry_identifier: str, register_class: type[Injectable]) -> None:
        if not issubclass(register_class, Injectable):
            raise RegistryError(self, "Registered class must be a subclass of Injectable")
        self._injectables[registry_identifier] = register_class

    def find[T: Injectable](self, *, by_type: type[T]) -> dict[str, type[T]]:
        return {registry_id: cls for registry_id, cls in self._injectables.items() if issubclass(cls, by_type)}

    def find_one[T: Injectable](self, *, by_identifier: str, by_type: type[T]) -> type[T]:
        injectable = self.find(by_type=by_type).get(by_identifier)
        if injectable is None:
            raise InjectableNotFoundError(
                by_identifier,
                self,
            )
        return injectable

    def get_pipe(self, *, by_identifier: str) -> type[Pipe]:
        return self.find_one(by_identifier=by_identifier, by_type=Pipe)

    def get_injectable(self, *, by_identifier: str) -> type[Injectable]:
        return self.find_one(by_identifier=by_identifier, by_type=Injectable)

    def get_available_injectables(self) -> Iterable[str]:
        return self._injectables.keys()
