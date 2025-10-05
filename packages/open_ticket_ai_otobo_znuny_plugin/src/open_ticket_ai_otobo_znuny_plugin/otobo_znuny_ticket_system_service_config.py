from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import BaseModel, SecretStr


class RawOTOBOZnunyTicketsystemServiceConfig(BaseModel):
    password: str
    base_url: str
    username: str = "open_ticket_ai"
    webservice_name: str = "OpenTicketAI"
    operation_urls: dict[str, str] = {
        TicketOperation.SEARCH.value: "ticket-search",
        TicketOperation.GET.value: "ticket-get",
        TicketOperation.UPDATE.value: "ticket-update",
    }


class RenderedOTOBOZnunyTicketsystemServiceConfig(BaseModel):
    password: SecretStr
    base_url: str
    username: str = "open_ticket_ai"
    webservice_name: str = "OpenTicketAI"
    operation_urls: dict[str, str] = {
        TicketOperation.SEARCH.value: "ticket-search",
        TicketOperation.GET.value: "ticket-get",
        TicketOperation.UPDATE.value: "ticket-update",
    }

    @property
    def operation_url_map(self) -> dict[TicketOperation, str]:
        return {TicketOperation(key): value for key, value in self.operation_urls.items()}

    def get_basic_auth(self) -> BasicAuth:
        return BasicAuth(user_login=self.username, password=self.password)

    def to_client_config(self) -> ClientConfig:
        return ClientConfig(
            base_url=self.base_url,
            webservice_name=self.webservice_name,
            operation_url_map=self.operation_url_map,
        )
