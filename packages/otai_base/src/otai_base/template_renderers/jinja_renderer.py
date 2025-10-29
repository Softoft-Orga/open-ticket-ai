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


class JinjaRenderer(TemplateRenderer):
    ParamsModel: ClassVar[type[BaseModel]] = StrictBaseModel

    @inject
    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory):
        super().__init__(config, logger_factory)
        self._jinja_env = NativeEnvironment(trim_blocks=True, lstrip_blocks=True, enable_async=True)

    async def _render(self, template_str: str, context: dict[str, Any]) -> Any:
        self._jinja_env.globals.update(context)
        self._jinja_env.globals["at_path"] = at_path
        self._jinja_env.globals["has_failed"] = has_failed
        self._jinja_env.globals["get_pipe_result"] = get_pipe_result
        self._jinja_env.globals["get_env"] = get_env
        self._jinja_env.globals["get_parent_param"] = get_parent_param
        self._jinja_env.globals["fail"] = fail
        template = self._jinja_env.from_string(template_str)
        return await template.render_async(context)
