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
            raise ValueError("Registered class must be a subclass of Pipe or Injectable")

    def get_pipe(self, registry_identifier: str) -> type[Pipe] | None:
        return self._pipes.get(registry_identifier)

    def get_injectable(self, registry_identifier: str) -> type[Injectable] | None:
        return self._services.get(registry_identifier)
