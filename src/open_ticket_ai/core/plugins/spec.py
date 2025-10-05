from __future__ import annotations

from typing import Any, Protocol, TypedDict


class PluginMetadata(TypedDict):
    name: str
    version: str
    core_api: str


class PluginHookSpec(Protocol):
    def get_metadata(self) -> PluginMetadata:
        ...

    def register_services(self, binder: Any) -> None:
        ...

    def register_pipes(self, factory: Any) -> None:
        ...
