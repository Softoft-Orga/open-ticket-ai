from collections.abc import Iterable
from numbers import Real
from typing import Any, ClassVar

from injector import inject
from jinja2.nativetypes import NativeEnvironment
from open_ticket_ai import InjectableConfig, LoggerFactory, StrictBaseModel, TemplateRenderer
from pydantic import BaseModel

from otai_base.template_renderers.jinja_renderer_extras import (
    at_path,
    fail,
    get_env,
    get_parent_param,
    get_pipe_result,
    has_failed,
)


class _SQLFragment:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


def _to_sql_literal(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, Real) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    msg = f"Unsupported value type: {type(value).__name__}"
    raise TypeError(msg)


def sql(value: Any) -> _SQLFragment:
    return _SQLFragment(_to_sql_literal(value))


def sql_list(values: Iterable[Any]) -> _SQLFragment:
    if isinstance(values, (str, bytes)):
        msg = "sql_list expects a non-string iterable"
        raise TypeError(msg)
    rendered_values = [str(sql(value)) for value in values]
    if not rendered_values:
        raise ValueError("sql_list requires at least one value")
    return _SQLFragment(f"({', '.join(rendered_values)})")


def _resolve_sql_fragments(value: Any) -> Any:
    if isinstance(value, _SQLFragment):
        return str(value)
    if isinstance(value, list):
        return [_resolve_sql_fragments(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_resolve_sql_fragments(item) for item in value)
    if isinstance(value, set):
        return {_resolve_sql_fragments(item) for item in value}
    if isinstance(value, dict):
        return {key: _resolve_sql_fragments(item) for key, item in value.items()}
    return value


class JinjaRenderer(TemplateRenderer):
    ParamsModel: ClassVar[type[BaseModel]] = StrictBaseModel

    @inject
    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory):
        super().__init__(config, logger_factory)
        self._jinja_env = NativeEnvironment(trim_blocks=True, lstrip_blocks=True, enable_async=True)
        self._jinja_env.filters.update({"sql": sql, "sql_list": sql_list})

    async def _render(self, template_str: str, context: dict[str, Any]) -> Any:
        self._jinja_env.globals.update(context)
        self._jinja_env.globals["at_path"] = at_path
        self._jinja_env.globals["has_failed"] = has_failed
        self._jinja_env.globals["get_pipe_result"] = get_pipe_result
        self._jinja_env.globals["get_env"] = get_env
        self._jinja_env.globals["get_parent_param"] = get_parent_param
        self._jinja_env.globals["fail"] = fail
        template = self._jinja_env.from_string(template_str)
        rendered = await template.render_async(context)
        return _resolve_sql_fragments(rendered)
