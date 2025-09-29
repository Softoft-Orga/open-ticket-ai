import ast
import json
import logging
from typing import Any

from jinja2 import Undefined, UndefinedError
from jinja2.sandbox import SandboxedEnvironment
from pydantic import BaseModel


class StrictUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        raise UndefinedError(f"Variable '{self._undefined_name}' is not defined in template")

    def __getattr__(self, name):
        raise UndefinedError(f"Variable '{self._undefined_name}.{name}' is not defined in template")

    def __getitem__(self, name):
        raise UndefinedError(f"Variable '{self._undefined_name}[{name!r}]' is not defined in template")

    def __str__(self):
        raise UndefinedError(f"Variable '{self._undefined_name}' is not defined in template")

    def __call__(self, *args, **kwargs):
        raise UndefinedError(f"Variable '{self._undefined_name}' is not defined in template")


_env = SandboxedEnvironment(autoescape=False, trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined)


def _parse_rendered_value(s: str) -> Any:
    if not s.strip():
        return s
    try:
        return json.loads(s)
    except Exception as e:
        logging.warning(f"Failed to parse JSON: {str(e)}")
        try:
            return ast.literal_eval(s)
        except Exception as e:
            logging.warning(f"Failed to parse literal: {str(e)}")
            return s


def render(template_str: str, scope: BaseModel | dict[str, Any]) -> Any:
    if isinstance(scope, BaseModel):
        scope_dict = scope.model_dump()
    else:
        scope_dict = scope

    try:
        template = _env.from_string(template_str)
        rendered = template.render(scope_dict)
        return _parse_rendered_value(rendered)
    except UndefinedError as e:
        logging.exception(f"Template variable not defined: {e}")
        raise
    except Exception as e:
        logging.exception(f"Template rendering failed: {e}")
        raise


def render_recursive(obj: Any, scope: BaseModel | dict[str, Any]) -> Any:
    if isinstance(scope, BaseModel):
        scope_dict = scope.model_dump()
    else:
        scope_dict = scope

    if isinstance(obj, str):
        return render(obj, scope_dict)
    elif isinstance(obj, list):
        return [render_recursive(item, scope_dict) for item in obj]
    elif isinstance(obj, dict):
        return {key: render_recursive(value, scope_dict) for key, value in obj.items()}
    else:
        return obj


class LazyTemplate:
    """Lazy-evaluated template that renders on first access."""

    def __init__(self, template_str: str, scope: dict[str, Any]):
        self._template_str = template_str
        self._scope = scope
        self._is_rendered = False
        self._value: Any = None

    def __str__(self) -> str:
        if not self._is_rendered:
            self._value = render(self._template_str, self._scope)
            self._is_rendered = True
        return str(self._value)

    def __repr__(self) -> str:
        return f"LazyTemplate({self._template_str!r})"


def render_text(value: Any, scope: dict[str, Any]) -> Any:
    """Render text value, returning LazyTemplate for strings."""
    if isinstance(value, str):
        return LazyTemplate(value, scope)
    return value


def render_any(value: Any, scope: dict[str, Any]) -> Any:
    """Render any value recursively."""
    return render_recursive(value, scope)
