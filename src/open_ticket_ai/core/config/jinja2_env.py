import ast
import json
import logging
from typing import Any

from jinja2.sandbox import SandboxedEnvironment
from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry


_env = SandboxedEnvironment(autoescape=False, trim_blocks=True, lstrip_blocks=True)


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


def render(template_str: str, scope: BaseModel | dict[str, Any], fail_silently: bool = False) -> Any:
    if isinstance(scope, BaseModel):
        scope = scope.model_dump()
    try:
        template = _env.from_string(template_str)
        rendered = template.render(scope)
        return _parse_rendered_value(rendered)
    except Exception as e:
        logging.exception(f"Template rendering failed: {e}")
        if fail_silently:
            return template_str
        raise e


def render_recursive(obj: Any, scope: BaseModel | dict[str, Any], fail_silently: bool = False) -> list | dict | str:
    if isinstance(scope, BaseModel):
        scope = scope.model_dump()

    if isinstance(obj, str):
        return render(obj, scope, fail_silently)
    elif isinstance(obj, list):
        return [render_recursive(item, scope, fail_silently) for item in obj]
    elif isinstance(obj, dict):
        return {key: render_recursive(value, scope, fail_silently) for key, value in obj.items()}
    else:
        raise RuntimeError(f"Unsupported type: {type(obj)}")
