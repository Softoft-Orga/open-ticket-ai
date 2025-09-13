from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable


class Registry:
    "Key→class registry for Providable."

    def __init__(self):
        self._map: dict[str, type[Providable]] = {}

    def register_all(self, instance_classes: list[type[Providable]]) -> None:
        for cls in instance_classes:
            self.register(cls)

    def register[T: Providable](self, instance_class: type[T]) -> None:
        self._map[instance_class.get_provider_key()] = instance_class

    def get[T: Providable](self, registry_instance_key: str, instance_class: type[T]) -> type[T]:
        try:
            registered_class = self._map[registry_instance_key]
        except KeyError:
            raise KeyError(f"Registry instance key '{registry_instance_key}' not found.")
        if not issubclass(registered_class, instance_class):
            raise TypeError(f"Registered class {registered_class} is not a subclass of {instance_class}.")
        return registered_class

    def contains(self, registry_instance_key: str) -> bool:
        return registry_instance_key in self._map

    def get_registry_types_descriptions(self) -> str:
        return "\n".join(f"{cls.get_provider_key()}: {cls.get_description()}" for cls in
                         self._map.values()) or "No registered types found."

    def get_all_registry_keys(self) -> list[str]:
        return list(self._map.keys())

    def get_type_from_key(self, registry_instance_key: str) -> type[Providable]:
        try:
            return self._map[registry_instance_key]
        except KeyError:
            raise KeyError(f"Registry instance key '{registry_instance_key}' not found.")
