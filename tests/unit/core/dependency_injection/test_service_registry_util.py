from unittest.mock import MagicMock

import pytest

from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.base.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.config.errors import InjectableNotFoundError
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.dependency_injection.service_registry_util import find_all_configured_services_of_type
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from tests.unit.conftest import SimpleInjectable


class MockOTOBOZnunyTicketSystemService(TicketSystemService):
    @staticmethod
    def get_params_model() -> type:
        from pydantic import BaseModel
        return BaseModel

    async def update_ticket(self, ticket_id: str, updates):
        pass

    async def find_tickets(self, criteria):
        pass

    async def find_first_ticket(self, criteria):
        pass

    async def add_note(self, ticket_id: str, note):
        pass


class MockHFClassificationService(Injectable):
    @staticmethod
    def get_params_model() -> type:
        from pydantic import BaseModel
        return BaseModel


class TestFindAllConfiguredServicesOfType:
    def test_find_matching_template_renderer_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("otobo_service", MockOTOBOZnunyTicketSystemService)
        registry.register("hf_service", MockHFClassificationService)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="ticket_system1", use="otobo_service"),
            InjectableConfig(id="ai_service1", use="hf_service"),
        ]

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0].id == "renderer1"
        assert result[0].use == "jinja_renderer"

    def test_find_matching_ticket_system_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("otobo_service", MockOTOBOZnunyTicketSystemService)
        registry.register("hf_service", MockHFClassificationService)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="ticket_system1", use="otobo_service"),
            InjectableConfig(id="ai_service1", use="hf_service"),
        ]

        result = find_all_configured_services_of_type(configs, registry, TicketSystemService)

        assert len(result) == 1
        assert result[0].id == "ticket_system1"
        assert result[0].use == "otobo_service"

    def test_find_all_injectable_configs(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("otobo_service", MockOTOBOZnunyTicketSystemService)
        registry.register("hf_service", MockHFClassificationService)

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="ticket_system1", use="otobo_service"),
            InjectableConfig(id="ai_service1", use="hf_service"),
        ]

        result = find_all_configured_services_of_type(configs, registry, Injectable)

        assert len(result) == 3
        assert {c.id for c in result} == {"renderer1", "ticket_system1", "ai_service1"}

    def test_empty_list_when_no_matching_configs(self):
        registry = ComponentRegistry()
        registry.register("otobo_service", MockOTOBOZnunyTicketSystemService)
        registry.register("hf_service", MockHFClassificationService)

        configs = [
            InjectableConfig(id="ticket_system1", use="otobo_service"),
            InjectableConfig(id="ai_service1", use="hf_service"),
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
                    InjectableConfig(id="ticket1", use="otobo_service"),
                ],
                TemplateRenderer,
                {"renderer1"},
            ),
            (
                [
                    InjectableConfig(id="renderer1", use="jinja_renderer"),
                    InjectableConfig(id="ticket1", use="otobo_service"),
                ],
                TicketSystemService,
                {"ticket1"},
            ),
            (
                [
                    InjectableConfig(id="renderer1", use="jinja_renderer"),
                    InjectableConfig(id="ticket1", use="otobo_service"),
                    InjectableConfig(id="hf1", use="hf_service"),
                ],
                Injectable,
                {"renderer1", "ticket1", "hf1"},
            ),
        ],
    )
    def test_parametrized_filtering_by_type(self, configs, filter_class, expected_ids):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)
        registry.register("otobo_service", MockOTOBOZnunyTicketSystemService)
        registry.register("hf_service", MockHFClassificationService)

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
        mock_registry.get_injectable.side_effect = [JinjaRenderer, MockHFClassificationService]

        configs = [
            InjectableConfig(id="renderer1", use="jinja_renderer"),
            InjectableConfig(id="hf1", use="hf_service"),
        ]

        result = find_all_configured_services_of_type(configs, mock_registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0].id == "renderer1"
        assert mock_registry.get_injectable.call_count == 2
        mock_registry.get_injectable.assert_any_call("jinja_renderer")
        mock_registry.get_injectable.assert_any_call("hf_service")

    def test_config_identity_preserved_in_result(self):
        registry = ComponentRegistry()
        registry.register("jinja_renderer", JinjaRenderer)

        original_config = InjectableConfig(
            id="renderer1",
            use="jinja_renderer",
            params={"custom_param": "value"},
            injects={"dep": "dependency"}
        )
        configs = [original_config]

        result = find_all_configured_services_of_type(configs, registry, TemplateRenderer)

        assert len(result) == 1
        assert result[0] is original_config
        assert result[0].params == {"custom_param": "value"}
        assert result[0].injects == {"dep": "dependency"}
