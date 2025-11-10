from datetime import timedelta

from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import BaseModel, Field

from otai_otobo_znuny.models import OTOBOZnunyTSServiceParams


class OtoboTestEnvironment(BaseModel):
    """Test environment configuration for OTOBO E2E tests"""

    monitored_queue: str = Field(description="Queue that is actively monitored and processed by the test workflows")
    cleanup_queue: str = Field(description="Queue where test tickets are moved for cleanup after tests")
    polling_interval: timedelta = Field(
        default=timedelta(seconds=5), description="How frequently the orchestrator checks for new tickets",
    )

    # Default ticket properties for test ticket creation
    default_state: str = Field(default="new", description="Default state for created test tickets")
    default_priority: str = Field(default="low", description="Default priority for created test tickets")
    default_type: str = Field(default="Incident", description="Default type for created test tickets")
    default_customer_user: str = Field(default="otai-demo-user", description="Default customer user for test tickets")


class OtoboE2EConfig(BaseModel):
    """Complete E2E test configuration for OTOBO integration"""

    service: OTOBOZnunyTSServiceParams
    environment: OtoboTestEnvironment


def create_otobo_e2e_config(
    *,
    password: str = "{{ get_env('OTAI_E2E_OTOBO_PASSWORD') }}",
    base_url: str = "http://3.66.72.29/otobo/nph-genericinterface.pl",
    username: str = "open_ticket_ai",
    webservice_name: str = "OpenTicketAI",
    monitored_queue: str = "~Test-Queue1",
    cleanup_queue: str = "~Test-Queue2",
    polling_interval: timedelta = timedelta(seconds=0.1),
    default_state: str = "new",
    default_priority: str = "medium",
    default_type: str = "Incident",
    default_customer_user: str = "otai-demo-user",
) -> OtoboE2EConfig:
    """
    Factory function to create OTOBO E2E configuration with sensible defaults.

    Args:
        password: OTOBO API password (reads from OTAI_E2E_OTOBO_PASSWORD env var if not provided)
        base_url: OTOBO instance base URL
        username: OTOBO API username
        webservice_name: Name of the OTOBO web service
        monitored_queue: Queue to monitor in tests
        cleanup_queue: Queue for cleaning up test tickets
        polling_interval: How often to poll for tickets
        default_state: Default ticket state for test tickets
        default_priority: Default ticket priority for test tickets
        default_type: Default ticket type for test tickets
        default_customer_user: Default customer user for test tickets

    Returns:
        Configured OtoboE2EConfig instance

    Raises:
        ValueError: If password is not provided and OTAI_E2E_OTOBO_PASSWORD is not set
    """

    return OtoboE2EConfig(service=(OTOBOZnunyTSServiceParams(
        base_url=base_url,
        username=username,
        password=password,
        webservice_name=webservice_name,
        operation_urls={
            TicketOperation.CREATE.value: "ticket-create",
            TicketOperation.SEARCH.value: "ticket-search",
            TicketOperation.GET.value: "ticket-get",
            TicketOperation.UPDATE.value: "ticket-update",
        },
    )), environment=(OtoboTestEnvironment(
        monitored_queue=monitored_queue,
        cleanup_queue=cleanup_queue,
        polling_interval=polling_interval,
        default_state=default_state,
        default_priority=default_priority,
        default_type=default_type,
        default_customer_user=default_customer_user,
    )))
