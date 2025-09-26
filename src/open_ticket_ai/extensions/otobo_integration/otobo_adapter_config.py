# FILE_PATH: open_ticket_ai\src\ce\ticket_system_integration\otobo_adapter_config.py
import os

from pydantic import BaseModel


class OTOBOAdapterConfig(BaseModel):
    server_address: str
    webservice_name: str
    search_operation_url: str
    update_operation_url: str
    get_operation_url: str
    username: str
    password_env_var: str

    @property
    def password(self) -> str:
        password = os.getenv(self.password_env_var)
        if not password:
            raise ValueError(f"Environment variable '{self.password_env_var}' is not set.")
        return password
