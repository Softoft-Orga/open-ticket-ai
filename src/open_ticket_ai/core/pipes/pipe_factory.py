from typing import Any

from async_lru import alru_cache
from injector import inject, singleton
from pydantic import BaseModel

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
        self._logger = logger_factory.create(self.__class__.__name__)
        self._service_configs: list[InjectableConfig] = otai_config.get_services_list()
        self._component_registry = component_registry

    @alru_cache()
    async def create_pipe(self, pipe_config: PipeConfig, pipe_context: PipeContext) -> Pipe:
        injected_services = await self._resolve_service_injects(pipe_config.injects)
        pipe_class: type[Pipe] = self._component_registry.get_pipe(by_identifier=pipe_config.use)

        rendered_params: BaseModel = await self._template_renderer.render_to_model(
            to_model=pipe_class.ParamsModel, from_raw_dict=pipe_config.params, with_scope=pipe_context.model_dump()
        )

        rendered_config = pipe_config.model_copy(update={"params": rendered_params.model_dump()})

        return pipe_class(
            config=rendered_config,
            pipe_context=pipe_context,
            logger_factory=self._logger_factory,
            pipe_factory=self,
            **injected_services,
        )

    async def _resolve_service_injects(self, injects: dict[str, str]) -> dict[str, Any]:
        return {param_name: await self._get_service_by_id(service_id) for param_name, service_id in injects.items()}

    async def _get_service_by_id(self, service_id: str) -> Injectable:
        config: InjectableConfig | None = next(
            (service_config for service_config in self._service_configs if service_config.id == service_id), None
        )
        if config is None:
            raise NoServiceConfigurationFoundError(service_id, self._service_configs)

        injectable_class: type[Injectable] = self._component_registry.get_injectable(by_identifier=config.use)
        rendered_params: BaseModel = await self._template_renderer.render_to_model(
            to_model=injectable_class.ParamsModel, from_raw_dict=config.params, with_scope={}
        )
        rendered_config = config.model_copy(update={"params": rendered_params.model_dump()})

        return injectable_class(
            config=rendered_config,
            logger_factory=self._logger_factory,
        )
