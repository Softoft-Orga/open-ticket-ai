import pytest
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr

from open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service_config import (
    RenderedOTOBOZnunyTicketsystemServiceConfig,
)


class TestRenderedOTOBOZnunyTicketsystemServiceConfig:
    @pytest.fixture
    def basic_config(self):
        return RenderedOTOBOZnunyTicketsystemServiceConfig(
            password=SecretStr("test_password"),
            base_url="https://otobo.example.com",
            username="test_user",
            webservice_name="TestService",
        )

    @pytest.fixture
    def custom_config(self):
        return RenderedOTOBOZnunyTicketsystemServiceConfig(
            password=SecretStr("custom_pass"),
            base_url="https://custom.otobo.com",
            username="custom_user",
            webservice_name="CustomService",
            operation_urls={"SEARCH": "custom-search", "GET": "custom-get", "UPDATE": "custom-update"},
        )

    def test_default_values(self):
        config = RenderedOTOBOZnunyTicketsystemServiceConfig(password=SecretStr("pass"), base_url="https://test.com")

        assert config.username == "open_ticket_ai"
        assert config.webservice_name == "OpenTicketAI"
        assert config.operation_urls == {"SEARCH": "ticket-search", "GET": "ticket-get", "UPDATE": "ticket-update"}

    def test_password_is_secret(self, basic_config):
        assert isinstance(basic_config.password, SecretStr)
        assert basic_config.password.get_secret_value() == "test_password"

    def test_operation_url_map_property(self, basic_config):
        url_map = basic_config.operation_url_map

        assert isinstance(url_map, dict)
        assert url_map[TicketOperation.SEARCH] == "ticket-search"
        assert url_map[TicketOperation.GET] == "ticket-get"
        assert url_map[TicketOperation.UPDATE] == "ticket-update"
        assert len(url_map) == 3

    def test_operation_url_map_with_custom_urls(self, custom_config):
        url_map = custom_config.operation_url_map

        assert url_map[TicketOperation.SEARCH] == "custom-search"
        assert url_map[TicketOperation.GET] == "custom-get"
        assert url_map[TicketOperation.UPDATE] == "custom-update"

    def test_get_basic_auth(self, basic_config):
        auth = basic_config.get_basic_auth()

        assert isinstance(auth, BasicAuth)
        assert auth.user_login == "test_user"
        assert auth.password == basic_config.password

    def test_get_basic_auth_with_custom_credentials(self, custom_config):
        auth = custom_config.get_basic_auth()

        assert auth.user_login == "custom_user"
        assert auth.password.get_secret_value() == "custom_pass"

    def test_to_client_config(self, basic_config):
        client_config = basic_config.to_client_config()

        assert isinstance(client_config, ClientConfig)
        assert client_config.base_url == "https://otobo.example.com"
        assert client_config.webservice_name == "TestService"
        assert client_config.operation_url_map == basic_config.operation_url_map

    def test_to_client_config_with_custom_values(self, custom_config):
        client_config = custom_config.to_client_config()

        assert client_config.base_url == "https://custom.otobo.com"
        assert client_config.webservice_name == "CustomService"
        assert client_config.operation_url_map[TicketOperation.SEARCH] == "custom-search"

    @pytest.mark.parametrize(
        "operation_str,operation_enum",
        [
            ("SEARCH", TicketOperation.SEARCH),
            ("GET", TicketOperation.GET),
            ("UPDATE", TicketOperation.UPDATE),
        ],
    )
    def test_operation_url_map_converts_string_to_enum(self, operation_str, operation_enum):
        config = RenderedOTOBOZnunyTicketsystemServiceConfig(
            password=SecretStr("pass"),
            base_url="https://test.com",
            operation_urls={operation_str: f"test-{operation_str.lower()}"},
        )

        url_map = config.operation_url_map
        assert operation_enum in url_map
        assert url_map[operation_enum] == f"test-{operation_str.lower()}"

    def test_config_immutability(self, basic_config):
        original_username = basic_config.username
        original_url = basic_config.base_url

        basic_config_dict = basic_config.model_dump()
        basic_config_dict["username"] = "modified_user"
        basic_config_dict["base_url"] = "https://modified.com"

        assert basic_config.username == original_username
        assert basic_config.base_url == original_url


class TestRawOTOBOZnunyTicketsystemServiceConfig:
    def test_inherits_from_base_config(self):
        config = RawOTOBOZnunyTicketsystemServiceConfig(password="raw_password", base_url="https://raw.example.com")

        assert config.password == "raw_password"
        assert config.base_url == "https://raw.example.com"
        assert config.username == "open_ticket_ai"
        assert config.webservice_name == "OpenTicketAI"

    def test_can_override_defaults(self):
        config = RawOTOBOZnunyTicketsystemServiceConfig(
            password="pass",
            base_url="https://test.com",
            username="custom_username",
            webservice_name="CustomWebService",
            operation_urls={"SEARCH": "my-search", "GET": "my-get", "UPDATE": "my-update"},
        )

        assert config.username == "custom_username"
        assert config.webservice_name == "CustomWebService"
        assert config.operation_urls["SEARCH"] == "my-search"

    @pytest.mark.parametrize(
        "base_url",
        [
            "https://otobo.local",
            "http://localhost:8080",
            "https://otobo.company.internal:443/api",
        ],
    )
    def test_various_base_urls(self, base_url):
        config = RawOTOBOZnunyTicketsystemServiceConfig(password="test", base_url=base_url)

        assert config.base_url == base_url
