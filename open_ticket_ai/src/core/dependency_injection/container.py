"""Dependency injection container setup for Open Ticket AI.

This module defines the `DIContainer` class which is the central dependency injection
container for the application. It also includes the `AppModule` which configures
the core bindings for the application.

The container is responsible for:
    - Loading and validating the application configuration
    - Creating a registry of available components
    - Binding core services (like the ticket system client)
    - Providing methods to retrieve configured instances and pipelines
"""
import os

from injector import Binder, Injector, Module, provider, singleton

from open_ticket_ai.src.core.config.config_models import (
    OpenTicketAIConfig,
    PipelineConfig,
    load_config, ProvidableConfig, )
from open_ticket_ai.src.core.config.config_validator import OpenTicketAIConfigValidator
from open_ticket_ai.src.core.dependency_injection.abstract_container import AbstractContainer
from open_ticket_ai.src.base.create_registry import create_registry
from open_ticket_ai.src.core.dependency_injection.registry import Registry
from open_ticket_ai.src.core.mixins.registry_providable_instance import (
    Providable,
)
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.util.path_util import find_python_code_root_path
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.pipeline import Pipeline
from open_ticket_ai.src.base.otobo_integration import OTOBOAdapterConfig
from otobo import AuthData, OTOBOClient, OTOBOClientConfig, TicketOperation

"""Path to the configuration file.

Determined by:
1. `OPEN_TICKET_AI_CONFIG` environment variable if set
2. Defaults to `config.yml` in the project's root directory
"""
CONFIG_PATH = os.getenv('OPEN_TICKET_AI_CONFIG', find_python_code_root_path() / 'config.yml')


class AppModule(Module):
    """Injector module that binds the validated configuration."""

    def configure(self, binder: Binder):
        """Bind core configuration objects.

        Args:
            binder: The Injector binder used to configure bindings.
        """
        open_ticket_ai_config = load_config(CONFIG_PATH)
        registry = create_registry()
        binder.bind(OpenTicketAIConfig, to=open_ticket_ai_config, scope=singleton)
        binder.bind(Registry, to=registry, scope=singleton)
        binder.bind(Orchestrator, to=Orchestrator, scope=singleton)

    @provider
    @singleton
    def provide_validator(
        self,
        config: OpenTicketAIConfig,
        registry: Registry
    ) -> OpenTicketAIConfigValidator:
        """Provide a configuration validator instance.

        Args:
            config: The application configuration to validate.
            registry: The registry of available components.

        Returns:
            OpenTicketAIConfigValidator: The validator instance.
        """
        return OpenTicketAIConfigValidator(config, registry)

    @provider
    @singleton
    def provide_otobo_client(self, config: OpenTicketAIConfig) -> OTOBOClient:
        """Create an `OTOBOClient` using the system configuration.

        Args:
            config: The application configuration containing system parameters.

        Returns:
            OTOBOClient: Configured OTOBO client.
        """
        otobo_config = OTOBOAdapterConfig.model_validate(config.system.params)
        # noinspection PyArgumentList
        return OTOBOClient(
            config=OTOBOClientConfig(
                base_url=otobo_config.server_address,
                service=otobo_config.service_name,
                auth=AuthData(
                    UserLogin=otobo_config.user,
                    Password=otobo_config.password
                ),
                operations={
                    TicketOperation.SEARCH.value: otobo_config.search_operation_url,
                    TicketOperation.GET.value: otobo_config.get_operation_url,
                    TicketOperation.UPDATE.value: otobo_config.update_operation_url,
                }
            )
        )


class DIContainer(Injector, AbstractContainer):
    """Dependency injection container for Open Ticket AI.

    This container manages the application's dependency graph using Injector.
    It binds core components like configuration, registry, and orchestrator,
    and provides methods to retrieve configured instances.

    Attributes:
        config: Validated application configuration
        registry: Registry of available components
    """

    def __init__(self):
        """Initializes the dependency injection container.

        Performs the following setup:
        1. Initializes the Injector superclass with AppModule bindings
        2. Binds core configuration and registry as instance attributes
        3. Creates and binds the TicketSystemAdapter instance based on configuration
        """
        super().__init__([AppModule()])
        self.config: OpenTicketAIConfig = self.get(OpenTicketAIConfig)
        self.registry = self.get(Registry)

        system_adapter_class = self.registry.get_type_from_key(self.config.system.provider_key)
        system_adapter_instance = self.create_object(
            system_adapter_class,
            additional_kwargs={"config": self.config.system}
        )
        self.binder.bind(TicketSystemAdapter, to=system_adapter_instance, scope=singleton)

    def get_instance_config(self, id: str) -> ProvidableConfig:
        """Retrieve the configuration for a specific instance by its ID.

        Args:
            id: The unique identifier of the instance configuration to retrieve.

        Returns:
            The configuration object for the specified instance.

        Raises:
            KeyError: If no configuration is found for the given ID.
        """
        instance_config = next(
            (c for c in self.config.get_all_register_instance_configs() if c.id == id), None)
        if not instance_config:
            raise KeyError(f"Unknown instance ID: {id}")
        return instance_config

    def get_pipeline_config(self, id: str) -> PipelineConfig:
        """Retrieve the pipeline configuration for a specific pipeline by its ID.

        Args:
            id: The unique identifier of the pipeline configuration to retrieve.

        Returns:
            PipelineConfig: The configuration object for the specified pipeline.

        Raises:
            KeyError: If no pipeline configuration is found for the given ID.
        """
        pipeline_config = next(
            (c for c in self.config.pipelines if c.id == id), None)
        if not pipeline_config:
            raise KeyError(f"Unknown pipeline ID: {id}")
        return pipeline_config

    def get_instance[T: Providable](self, id: str, subclass_of: type[T]) -> T:
        """Retrieve a configured instance from the registry.

        Looks up the configuration by ID, retrieves the corresponding class from the registry,
        and creates an instance of that class. The instance must be a subclass of `Providable`
        and of the type specified by `subclass_of`.

        Args:
            id: Unique identifier of the instance configuration.
            subclass_of: The expected base class or interface of the instance (a subclass of `Providable`).

        Returns:
            T: Instantiated object of the requested type.

        Raises:
            KeyError: If configuration for the given `id` is not found, or if the provider key
                in the configuration is not found in the registry.
        """
        instance_config = self.get_instance_config(id)
        instance_class = self.registry.get(instance_config.provider_key, subclass_of)
        if not instance_class:
            raise KeyError(f"Unknown provider key: {instance_config.provider_key}")
        return self.create_object(instance_class, additional_kwargs={"config": instance_config})

    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        """Construct a processing pipeline instance.

        The pipeline is built from the configuration identified by `predictor_id`. It consists of:
        - A configuration for the entire pipeline (of type `PipelineConfig`)
        - A sequence of instantiated `Pipe` objects for each step in the pipeline.

        The pipeline itself is an instance of `Pipeline` (a subclass of `Pipe`), which chains the steps.

        Args:
            pipeline_id: The unique identifier of the pipeline configuration.

        Returns:
            Pipe: The constructed pipeline instance (a `Pipeline` object).

        Raises:
            KeyError: If the configuration for `predictor_id` is not found, or if the provider key
                in the configuration is not found in the registry.
        """
        pipeline_config: PipelineConfig | None = None
        try:
            pipeline_config = self.get_pipeline_config(pipeline_id)
            pipe_instances = [
                self.get_instance(pipe_id, Pipe)
                for pipe_id in pipeline_config.pipe_ids
            ]

        except KeyError:
            if pipeline_config:
                raise KeyError(f"Unknown predictor key: {pipeline_config.provider_key}")
            raise KeyError(f"Unknown predictor ID: {pipeline_id}")
        return Pipeline(
            config=pipeline_config,
            pipes=pipe_instances
        )
