from unittest.mock import MagicMock

import pytest
from otai_base.template_renderers.jinja_renderer import JinjaRenderer
from pydantic import BaseModel

from open_ticket_ai.core.config.errors import InjectableNotFoundError
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.service_registry_util import find_all_configured_services_of_type
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from tests.unit.conftest import SimpleInjectable


class RegistryTestInjectable1(Injectable):
    ParamsModel: type[BaseModel]


class RegistryTestInjectable2(Injectable):
    ParamsModel: type[BaseModel]


class TestFindAllConfiguredServicesOfType:
    def test_find_matching_template_renderer_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("test_injectable1", RegistryTestInjectable1)
        registry.register("test_injectable2", RegistryTestInjectable2)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="injectable1", use="test_injectable1"),
            InjectableConfig(id="injectable2", use="test_injectable2"),
        ]

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0].id == "renderer1"
        assert result[0].use == "jinja_renderer"

    def test_find_all_injectable_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("test_injectable1", RegistryTestInjectable1)
        registry.register("test_injectable2", RegistryTestInjectable2)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="injectable1", use="test_injectable1"),
            InjectableConfig(id="injectable2", use="test_injectable2"),
        ]

        result = find_all_configured_services_of_type(configs, registry, Injectable)

        assert len(result) == 3
        assert {c.id for c in result} == {"renderer1", "injectable1", "injectable2"}

    def test_empty_list_when_no_matching_configs(self):
        registry = ComponentRegistry()
        registry.register("test_injectable1", RegistryTestInjectable1)
        registry.register("test_injectable2", RegistryTestInjectable2)

        configs = [
            InjectableConfig(id="injectable1", use="test_injectable1"),
            InjectableConfig(id="injectable2", use="test_injectable2"),
        ]

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert result == []

    def test_empty_list_when_empty_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)

        configs = []

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert result == []

    def test_handles_multiple_configs_of_same_type(self):
        registry = ComponentRegistry()
        registry.register("simple1", SimpleInjectable)
        registry.register("simple2", SimpleInjectable)
        registry.register("simple3", SimpleInjectable)

        configs = [
            InjectableConfig(id="service1", use="simple1"),
            InjectableConfig(id="service2", use="simple2"),
            InjectableConfig(id="service3", use="simple3"),
        ]

        result = find_all_configured_services_of_type(configs, registry, SimpleInjectable)

        assert len(result) == 3
        assert {c.id for c in result} == {"service1", "service2", "service3"}

    @pytest.mark.parametrize(
        "configs,filter_class,expected_ids",
        [
            (
                [
                    InjectableConfig(id="renderer1", use="jinja_renderer"),
                    InjectableConfig(id="injectable1", use="test_injectable1"),
                ],
                TemplateRenderer,
                {"renderer1"},
            ),
            (
                [
                    InjectableConfig(id="renderer1", use="jinja_renderer"),
                    InjectableConfig(id="injectable1", use="test_injectable1"),
                ],
                RegistryTestInjectable1,
                {"injectable1"},
            ),
            (
                [
                    InjectableConfig(id="renderer1", use="jinja_renderer"),
                    InjectableConfig(id="injectable1", use="test_injectable1"),
                    InjectableConfig(id="injectable2", use="test_injectable2"),
                ],
                Injectable,
                {"renderer1", "injectable1", "injectable2"},
            ),
        ],
    )
    def test_parametrized_filtering_by_type(self, configs, filter_class, expected_ids):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("test_injectable1", RegistryTestInjectable1)
        registry.register("test_injectable2", RegistryTestInjectable2)

        result = find_all_configured_services_of_type(configs, registry, filter_class)

        assert {c.id for c in result} == expected_ids

    def test_raises_error_when_injectable_not_found_in_registry(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="nonexistent", use="nonexistent_service"),
        ]

        with pytest.raises(InjectableNotFoundError):
            find_all_configured_services_of_type(configs, registry, TemplateRenderer)

    def test_uses_component_registry_for_type_resolution(self):
        mock_registry = MagicMock(spec=ComponentRegistry)
        mock_registry.get_injectable.side_effect = [JinjaRenderer, RegistryTestInjectable1]

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="injectable1", use="test_injectable1"),
        ]

        result = find_all_configured_services_of_type(configs, mock_registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0].id == "renderer1"

    def test_config_identity_preserved_in_result(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)

        original_config = InjectableConfig(
            id="renderer1", use="jinja_renderer", params={"custom_param": "value"}, injects={"dep": "dependency"}
        )
        configs = [original_config]

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0] is original_config
        assert result[0].params == {"custom_param": "value"}
        assert result[0].injects == {"dep": "dependency"}
