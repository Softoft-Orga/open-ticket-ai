from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

from pydantic import SecretStr


def _install_otobo_stubs() -> None:
    """Provide minimal stubs for otobo_znuny dependencies used in tests."""

    if "otobo_znuny.domain_models.basic_auth_model" in sys.modules:
        return

    otobo_module = ModuleType("otobo_znuny")
    domain_models_module = ModuleType("otobo_znuny.domain_models")

    basic_auth_module = ModuleType("otobo_znuny.domain_models.basic_auth_model")

    @dataclass
    class BasicAuth:  # noqa: D401 - simple stub container
        user_login: str
        password: object

    basic_auth_module.BasicAuth = BasicAuth

    client_config_module = ModuleType("otobo_znuny.domain_models.otobo_client_config")

    @dataclass
    class ClientConfig:  # noqa: D401 - simple stub container
        base_url: str
        webservice_name: str
        operation_url_map: dict

    client_config_module.ClientConfig = ClientConfig

    ticket_operation_module = ModuleType("otobo_znuny.domain_models.ticket_operation")

    class TicketOperation(str, Enum):
        SEARCH = "SEARCH"
        GET = "GET"
        UPDATE = "UPDATE"

    ticket_operation_module.TicketOperation = TicketOperation

    sys.modules["otobo_znuny"] = otobo_module
    sys.modules["otobo_znuny.domain_models"] = domain_models_module
    sys.modules["otobo_znuny.domain_models.basic_auth_model"] = basic_auth_module
    sys.modules["otobo_znuny.domain_models.otobo_client_config"] = client_config_module
    sys.modules["otobo_znuny.domain_models.ticket_operation"] = ticket_operation_module

    otobo_module.domain_models = domain_models_module
    domain_models_module.basic_auth_model = basic_auth_module
    domain_models_module.otobo_client_config = client_config_module
    domain_models_module.ticket_operation = ticket_operation_module


_install_otobo_stubs()

from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation


def _load_config_module():
    module_path = (
        Path(__file__)
        .resolve()
        .parents[4]
        / "src"
        / "open_ticket_ai"
        / "otobo_znuny_plugin"
        / "otobo_znuny_ticket_system_service_config.py"
    )
    spec = spec_from_file_location("_otobo_config_module", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_config_module = _load_config_module()

RawOTOBOZnunyTicketsystemServiceConfig = _config_module.RawOTOBOZnunyTicketsystemServiceConfig
RenderedOTOBOZnunyTicketsystemServiceConfig = _config_module.RenderedOTOBOZnunyTicketsystemServiceConfig


def test_get_basic_auth_uses_config_credentials():
    password = SecretStr("pw")
    config = RenderedOTOBOZnunyTicketsystemServiceConfig(
        password=password,
        base_url="https://example.com",
        username="configured_user",
    )

    auth = config.get_basic_auth()

    assert isinstance(auth, BasicAuth)
    assert auth.user_login == "configured_user"
    assert auth.password is password


def test_to_client_config_builds_client_config_with_operation_map():
    config = RenderedOTOBOZnunyTicketsystemServiceConfig(
        password=SecretStr("pw"),
        base_url="https://api.example.com",
        webservice_name="Service",
    )

    client_config = config.to_client_config()

    assert isinstance(client_config, ClientConfig)
    assert client_config.base_url == "https://api.example.com"
    assert client_config.webservice_name == "Service"
    assert client_config.operation_url_map == config.operation_url_map


def test_raw_config_provides_default_values():
    raw_config = RawOTOBOZnunyTicketsystemServiceConfig(
        password="plain", base_url="https://raw.example.com"
    )

    assert raw_config.username == "open_ticket_ai"
    assert raw_config.operation_urls[TicketOperation.SEARCH.value] == "ticket-search"


def test_raw_config_allows_overrides():
    operation_urls = {"SEARCH": "search", "GET": "get", "UPDATE": "update"}
    raw_config = RawOTOBOZnunyTicketsystemServiceConfig(
        password="plain",
        base_url="https://raw.example.com",
        username="custom",
        operation_urls=operation_urls,
    )

    assert raw_config.username == "custom"
    assert raw_config.operation_urls == operation_urls
