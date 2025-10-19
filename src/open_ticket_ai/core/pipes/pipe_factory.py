from typing import Any

from injector import inject, singleton

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.core.config.errors import NoServiceConfigurationFoundError
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


@singleton
class PipeFactory:
    @inject
    def __init__(
            self,
            template_renderer: TemplateRenderer,
            logger_factory: LoggerFactory,
            otai_config: OpenTicketAIConfig,
            component_registry: ComponentRegistry,
    ):
        self._template_renderer = template_renderer
        self._logger_factory = logger_factory
        self._service_configs: list[InjectableConfig] = otai_config.get_services_list()
        self._component_registry = component_registry

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

        pipe_class = self._component_registry.get_pipe(pipe_config.use)

        return pipe_class(
            config=rendered_config,
            pipe_context=pipe_context,
            logger_factory=self._logger_factory,
            **injected_services,
        )

    def _resolve_service_injects(self, injects: dict[str, str]) -> dict[str, Any]:
        return {param_name: self._get_service_by_id(service_id) for param_name, service_id in injects.items()}

    def _get_service_by_id(self, service_id: str) -> Injectable:
        """
        TODO do not manually pass in dependencies to service constructor, since its unflexible.
        They should be injected. Use AssistedBuilder for services as well?
        """
        config = next(
            (service_config for service_config in self._service_configs if service_config.id == service_id),
            None
        )
        if config is None:
            raise NoServiceConfigurationFoundError(service_id, self._service_configs)

        registry_identifier = config.use
        cls: type[Injectable] = self._component_registry.get_injectable(registry_identifier)

        return cls(
            config=config,
            logger_factory=self._logger_factory,
        )
