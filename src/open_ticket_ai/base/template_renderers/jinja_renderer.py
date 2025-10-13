import logging
from typing import Any

from injector import inject
from jinja2.sandbox import SandboxedEnvironment

from open_ticket_ai.base.template_renderers.jinja_renderer_extras import (
    at_path,
    build_filtered_env,
    has_failed,
    pipe_result,
)
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


class JinjaRenderer(TemplateRenderer):
    @inject
    def __init__(
        self,
        config: JinjaRendererConfig,
    ):
        self.config = config
        self.jinja_env = SandboxedEnvironment(
            autoescape=config.autoescape, trim_blocks=config.trim_blocks, lstrip_blocks=config.lstrip_blocks
        )
        self._logger = logging.getLogger(self.__class__.__name__)

    def render(self, template_str: str, scope: dict[str, Any], fail_silently: bool = False) -> Any:
        self.jinja_env.globals.update(scope)
        self.jinja_env.globals["at_path"] = at_path
        self.jinja_env.globals["env"] = build_filtered_env(self.config)
        self.jinja_env.globals["has_failed"] = has_failed
        self.jinja_env.globals["pipe_result"] = pipe_result
        try:
            template = self.jinja_env.from_string(template_str)
            rendered = template.render(self._to_dict(scope))
            return self._parse_rendered_value(rendered)
        except Exception as e:
            self._logger.warning("Failed to render template '%s'", template_str)
            self._logger.warning("context: %s", scope)
            self._logger.exception("Template rendering failed")
            if fail_silently:
                return template_str
            raise RuntimeError(e) from e
