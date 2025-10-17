import typing
from pydoc import locate
from typing import Any

from injector import AssistedBuilder, Injector, inject, singleton

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering import TemplateRenderer


@singleton
class PipeFactory:
    @inject
    def __init__(
            self,
            injector: Injector,
            template_renderer: TemplateRenderer,
            logger_factory: LoggerFactory,
            otai_config: OpenTicketAIConfig,
    ):
        self._injector = injector
        self._template_renderer = template_renderer
        self._logger_factory = logger_factory
        self._service_configs: list[InjectableConfig] = otai_config.get_services_list()

    def render_pipe(self, pipe_config: PipeConfig, pipe_context: PipeContext) -> Pipe:
        """Create pipe with AssistedBuilder (factory renders config)."""

        injected_services = self._resolve_service_injects(pipe_config.injects)

        rendered_params = self._template_renderer.render(pipe_config.params, pipe_context.model_dump())

        rendered_config = PipeConfig(
            id=pipe_config.id,
            use=pipe_config.use,
            params=rendered_params,
            injects=pipe_config.injects,
            depends_on=pipe_config.depends_on,
        )

        pipe_class = locate(pipe_config.use)

        if not isinstance(pipe_class, type) or not issubclass(pipe_class, Pipe):
            raise TypeError(f"'{pipe_config.use}' is not a Pipe subclass!")
        pipe_class = typing.cast("type[Pipe]", pipe_class)
        builder = self._injector.get(AssistedBuilder[pipe_class])

        return builder.build(
            config=rendered_config,
            pipe_context=pipe_context,
            **injected_services,
        )

    def _resolve_service_injects(self, injects: dict[str, str]) -> dict[str, Any]:
        return {param_name: self._get_service_by_id(service_id) for param_name, service_id in injects.items()}

    def _get_service_by_id(self, service_id: str) -> Any:
        config = next((c for c in self._service_configs if c.id == service_id), None)
        if config is None:
            raise ValueError(f"Service '{service_id}' not found")

        cls = locate(config.use)
        if not isinstance(cls, type):
            raise TypeError(f"Service '{service_id}' is not a class")
        cls = typing.cast("type", cls)
        return cls(
            config=config,
            logger_factory=self._logger_factory,
        )
