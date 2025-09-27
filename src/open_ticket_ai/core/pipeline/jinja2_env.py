import ast
import json
import logging
from typing import Any

from jinja2 import Undefined
from jinja2.sandbox import SandboxedEnvironment

from open_ticket_ai.core.pipeline.context import PipelineContext


class LoggingUndefined(Undefined):
    def __getattr__(self, name):
        logging.warning(f"Undefined variable accessed: {self._undefined_name}.{name}")
        return self._fail_with_undefined_error()

    def __getitem__(self, name):
        logging.warning(f"Undefined item accessed: {self._undefined_name}['{name}']")
        return self._fail_with_undefined_error()

    def __str__(self):
        logging.warning(f"Undefined variable used as string: {self._undefined_name}")
        return self._fail_with_undefined_error()


_env = SandboxedEnvironment(
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=LoggingUndefined
)

def render_text(val: Any, scope: dict):
    if not isinstance(val, str):
        return val
    try:
        template = _env.from_string(val)
        return template.render(scope)
    except Exception as e:
        logging.warning(f"Template rendering error: {str(e)}")
        return val

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

def render_any(obj: Any, scope: PipelineContext) -> Any:
    if isinstance(obj, str):
        rendered = render_text(obj, scope.model_dump())
        return _parse_rendered_value(rendered) if isinstance(rendered, str) else rendered
    if isinstance(obj, list):
        return [render_any(v, scope) for v in obj]
    if isinstance(obj, dict):
        return {k: render_any(v, scope) for k, v in obj.items()}
    logging.warning(f"Unsupported type: {type(obj)}")
    return obj
