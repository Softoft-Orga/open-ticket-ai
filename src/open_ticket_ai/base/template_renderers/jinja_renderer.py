from typing import Any

from injector import inject
from jinja2.nativetypes import NativeEnvironment
from pydantic import BaseModel

from open_ticket_ai.base.template_renderers.jinja_renderer_extras import at_path, fail, get_pipe_result, has_failed
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class JinjaRenderer(TemplateRenderer[StrictBaseModel]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return StrictBaseModel

    @inject
    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory):
        super().__init__(config, logger_factory)
        self._jinja_env = NativeEnvironment(trim_blocks=True, lstrip_blocks=True)

    def _render(self, template_str: str, context: dict[str, Any]) -> Any:
        self._jinja_env.globals.update(context)
        self._jinja_env.globals["at_path"] = at_path
        self._jinja_env.globals["has_failed"] = has_failed
        self._jinja_env.globals["get_pipe_result"] = get_pipe_result
        self._jinja_env.globals["fail"] = fail
        template = self._jinja_env.from_string(template_str)
        return template.render(context)
