from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr

from open_ticket_ai.core.config.raw_config import RawRegisterableConfig, RegisterableConfig, BaseRegisterableConfig, \
    RenderedRegistrableConfig


class _OTOBOZnunyTicketsystemServiceBaseConfig(BaseRegisterableConfig):
    password: str
    base_url: str
    username: str = "open_ticket_ai"
    webservice_name: str = "OpenTicketAI"
    operation_urls: dict[str, str] = {
        TicketOperation.SEARCH.value: "ticket-search",
        TicketOperation.GET.value: "ticket-get",
        TicketOperation.UPDATE.value: "ticket-update",
    }


class RenderedOTOBOZnunyTicketsystemServiceConfig(RenderedRegistrableConfig, _OTOBOZnunyTicketsystemServiceBaseConfig):
    password: SecretStr

    @property
    def operation_url_map(self) -> dict[TicketOperation, str]:
        return {
            TicketOperation(key): value
            for key, value in self.operation_urls.items()
        }

    def get_basic_auth(self) -> BasicAuth:
        return BasicAuth(
            user_login=self.username,
            password=self.password
        )

    def to_client_config(self) -> ClientConfig:
/* <<<<<<<<<<<<<<  ✨ Windsurf Command ⭐ >>>>>>>>>>>>>>>> */
    """
    Convert the rendered config to a client config.

    This method takes the rendered config and converts it into a client config
    that can be used to initialize the otobo client.

    Returns:
        ClientConfig: The client config that can be used to initialize the otobo client.
    """
/* <<<<<<<<<<  cfc74101-3770-41a7-b32b-1bc5ce449759  >>>>>>>>>>> */
        return ClientConfig(
            base_url=self.base_url,
            webservice_name=self.webservice_name,
            operation_url_map=self.operation_url_map,
        )


class RawOTOBOZnunyTicketsystemServiceConfig(RawRegisterableConfig, _OTOBOZnunyTicketsystemServiceBaseConfig):
    pass

