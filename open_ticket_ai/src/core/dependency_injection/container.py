# FILE_PATH: open_ticket_ai/src/core/dependency_injection/container.py
import os
from injector import Binder, Injector, Module, provider, singleton

from open_ticket_ai.src.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig
from open_ticket_ai.src.core.config.config_models import (
    OpenTicketAIConfig,
    PipelineConfig,
    ProvidableConfig,
    load_config,
)
from open_ticket_ai.src.core.config.config_validator import OpenTicketAIConfigValidator
from open_ticket_ai.src.core.dependency_injection.abstract_container import AbstractContainer
from open_ticket_ai.src.base.create_registry import create_registry
from open_ticket_ai.src.core.dependency_injection.registry import Registry
from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from open_ticket_ai.src.core.orchestrator import Orchestrator
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.util.path_util import find_python_code_root_path
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline
from otobo import AuthData, OTOBOClient, OTOBOClientConfig, TicketOperation

CONFIG_PATH = os.getenv("OPEN_TICKET_AI_CONFIG", find_python_code_root_path() / "config.yml")


class AppModule(Module):
    def configure(self, binder: Binder):
        config = load_config(CONFIG_PATH)
        registry = create_registry()
        binder.bind(OpenTicketAIConfig, to=config, scope=singleton)
        binder.bind(Registry, to=registry, scope=singleton)
        binder.bind(Orchestrator, to=Orchestrator, scope=singleton)

    @provider
    @singleton
    def provide_validator(self, config: OpenTicketAIConfig, registry: Registry) -> OpenTicketAIConfigValidator:
        return OpenTicketAIConfigValidator(config, registry)

    @provider
    @singleton
    def provide_otobo_client(self, config: OpenTicketAIConfig) -> OTOBOClient:
        oc = OTOBOAdapterConfig.model_validate(config.system.params)
        return OTOBOClient(
            config=OTOBOClientConfig(
                base_url=oc.server_address,
                service=oc.service_name,
                auth=AuthData(UserLogin=oc.user, Password=oc.password),
                operations={
                    TicketOperation.SEARCH.value: oc.search_operation_url,
                    TicketOperation.GET.value: oc.get_operation_url,
                    TicketOperation.UPDATE.value: oc.update_operation_url,
                },
            )
        )
    @provider
    @singleton
    def provide_ticket_system_adapter(
        self,
        injector: Injector,
        config: OpenTicketAIConfig,
        registry: Registry,
    ) -> TicketSystemAdapter:
        cls = registry.get(config.system.provider_key, TicketSystemAdapter)
        return injector.create_object(cls, additional_kwargs={"config": config.system})

    @provider
    @singleton
    def provide_orchestrator(
        self,
        injector: Injector,
        config: OpenTicketAIConfig,
        registry: Registry,
    ) -> Orchestrator:
        pipelines: list[Pipeline] = []
        for pc in config.pipelines:
            pipes = []
            for pipe_id in pc.pipes:
                inst_cfg = next((c for c in config.get_all_register_instance_configs() if c.id == pipe_id), None)
                if not inst_cfg:
                    raise KeyError(f"Unknown instance ID: {pipe_id}")
                cls = registry.get(inst_cfg.provider_key, Pipe)
                pipes.append(injector.create_object(cls, additional_kwargs={"config": inst_cfg}))
            pipelines.append(Pipeline(config=pc, pipes=pipes))
        return Orchestrator(pipelines=pipelines, config=config)


class DIContainer(Injector, AbstractContainer):
    def __init__(self):
        super().__init__([AppModule()])
        self.config: OpenTicketAIConfig = self.get(OpenTicketAIConfig)
        self.registry: Registry = self.get(Registry)

        system_adapter_class = self.registry.get(self.config.system.provider_key, TicketSystemAdapter)
        system_adapter_instance = self.create_object(system_adapter_class,
                                                     additional_kwargs={"config": self.config.system})
        self.binder.bind(TicketSystemAdapter, to=system_adapter_instance, scope=singleton)

    def get_instance_config(self, id: str) -> ProvidableConfig:
        cfg = next((c for c in self.config.get_all_register_instance_configs() if c.id == id), None)
        if not cfg:
            raise KeyError(f"Unknown instance ID: {id}")
        return cfg

    def get_pipeline_config(self, id: str) -> PipelineConfig:
        pc = next((c for c in self.config.pipelines if c.id == id), None)
        if not pc:
            raise KeyError(f"Unknown pipeline ID: {id}")
        return pc

    def get_instance[T: Providable](self, id: str, subclass_of: type[T]) -> T:
        inst_cfg = self.get_instance_config(id)
        cls = self.registry.get(inst_cfg.provider_key, subclass_of)
        return self.create_object(cls, additional_kwargs={"config": inst_cfg})

    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        pc = self.get_pipeline_config(pipeline_id)
        pipes = [self.get_instance(pipe_id, Pipe) for pipe_id in pc.pipes]
        return Pipeline(config=pc, pipes=pipes)
