from shutil import RegistryError

from open_ticket_ai.core.config.errors import InjectableNotFoundError
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.pipes.pipe import Pipe


class ComponentRegistry:
    def __init__(self):
        self._pipes: dict[str, type[Pipe]] = {}
        self._services: dict[str, type[Injectable]] = {}

    def register(self, registry_identifier: str, register_class: type[Injectable]):
        if issubclass(register_class, Pipe):
            self._pipes[registry_identifier] = register_class
        elif issubclass(register_class, Injectable):
            self._services[registry_identifier] = register_class
        else:
            raise RegistryError("Registered class must be a subclass of Pipe or Injectable")

    def get_pipe(self, registry_identifier: str) -> type[Pipe] | None:
        pipe = self._pipes.get(registry_identifier)
        if pipe is None:
            raise InjectableNotFoundError(
                registry_identifier,
                self,
            )
        return pipe

    def get_injectable(self, registry_identifier: str) -> type[Injectable]:
        service = self._services.get(registry_identifier)
        if service is None:
            raise InjectableNotFoundError(
                registry_identifier,
                self,
            )
        return service

    def find_by_type(self, cls: type[Injectable]) -> dict[str, type[Injectable]]:
        result = {}
        for registry_id, registered_cls in {**self._pipes, **self._services}.items():
            if issubclass(registered_cls, cls):
                result[registry_id] = registered_cls
        return result

    def get_available_injectables(self) -> list[str]:
        return list(self._services.keys()) + list(self._pipes.keys())
