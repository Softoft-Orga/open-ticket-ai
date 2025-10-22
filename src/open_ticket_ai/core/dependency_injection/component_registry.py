import logging

from open_ticket_ai.core.config.errors import InjectableNotFoundError, RegistryError
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.pipes.pipe import Pipe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComponentRegistry:
    def __init__(self) -> None:
        self._pipes: dict[str, type[Pipe]] = {}
        self._services: dict[str, type[Injectable]] = {}

    def register(self, registry_identifier: str, register_class: type[Injectable]) -> None:
        if issubclass(register_class, Pipe):
            self._pipes[registry_identifier] = register_class
            logger.info(f"Registered pipe: {registry_identifier}")
        elif issubclass(register_class, Injectable):
            self._services[registry_identifier] = register_class
            logger.info(f"Registered injectable: {registry_identifier}")
        else:
            raise RegistryError("Registered class must be a subclass of Pipe or Injectable")

    def get_pipe(self, registry_identifier: str) -> type[Pipe]:
        pipe = self._pipes.get(registry_identifier)
        if pipe is None:
            logger.warning(f"Pipe not found: {registry_identifier}")
            raise InjectableNotFoundError(
                registry_identifier,
                self,
            )
        logger.debug(f"Retrieved pipe: {registry_identifier}")
        return pipe

    def get_injectable(self, registry_identifier: str) -> type[Injectable]:
        service = self._services.get(registry_identifier)
        if service is None:
            logger.warning(f"Injectable not found: {registry_identifier}")
            raise InjectableNotFoundError(
                registry_identifier,
                self,
            )
        logger.debug(f"Retrieved injectable: {registry_identifier}")
        return service

    def find_by_type(self, cls: type[Injectable]) -> dict[str, type[Injectable]]:
        found = {
            registry_id: registered_cls
            for registry_id, registered_cls in {**self._pipes, **self._services}.items()
            if issubclass(registered_cls, cls)
        }
        logger.info(f"Found by type {cls.__name__}: {list(found.keys())}")
        return found

    def get_available_injectables(self) -> list[str]:
        available = list(self._services.keys()) + list(self._pipes.keys())
        logger.info(f"Available injectables: {available}")
        return available
