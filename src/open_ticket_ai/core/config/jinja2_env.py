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
        logging.error(f"Template variable not defined: {e}")
        raise
    except Exception as e:
        logging.error(f"Template rendering failed: {e}")
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


# Backward compatibility aliases
render_any = render_recursive
render_text = render


class LazyTemplate:
    def __init__(self, template_str: str):
        self.template_str = template_str
    
    def render(self, scope: BaseModel | dict[str, Any]) -> Any:
        return render(self.template_str, scope)
