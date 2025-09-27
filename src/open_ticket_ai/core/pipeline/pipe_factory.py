import importlib
from typing import Any

from injector import Injector

from open_ticket_ai.core.pipeline.base_pipe_config import BasePipeConfig
from open_ticket_ai.core.pipeline.pipe import Pipe


def _resolve_class(dotted_path: str) -> type[Pipe]:
    module_name, _, attr = dotted_path.rpartition(".")
    if not module_name or not attr:
        raise ValueError("class_path must be 'package.module.ClassName'")
    mod = importlib.import_module(module_name)
    cls = getattr(mod, attr, None)
    if cls is None:
        raise ValueError(f"{dotted_path} not found")
    return cls


def get_pipe_class(self) -> type:
    return _resolve_class(self.type)


def build_pipe(self, pipe_config: BasePipeConfig, container: Injector, **overrides: Any) -> Pipe:
    pipe_cls: type[Pipe] = _resolve_class(pipe_config.type)
    return container.create_object(
        pipe_cls,
        additional_kwargs={"config": self, **overrides},
    )
