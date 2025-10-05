from threading import Lock
from typing import Any, Callable

_registry_lock = Lock()
_template_methods: dict[str, Callable[..., Any]] = {}
_template_variables: dict[str, Callable[[], Any]] = {}


def jinja_template_method(method_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        with _registry_lock:
            _template_methods[method_name] = func
        return func
    return decorator


def jinja_variable(variable_name: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
    def decorator(func: Callable[[], Any]) -> Callable[[], Any]:
        with _registry_lock:
            _template_variables[variable_name] = func
        return func
    return decorator


def get_registered_methods() -> dict[str, Callable[..., Any]]:
    with _registry_lock:
        return dict(_template_methods)


def get_registered_variables() -> dict[str, Callable[[], Any]]:
    with _registry_lock:
        return dict(_template_variables)


def clear_registry() -> None:
    with _registry_lock:
        _template_methods.clear()
        _template_variables.clear()

