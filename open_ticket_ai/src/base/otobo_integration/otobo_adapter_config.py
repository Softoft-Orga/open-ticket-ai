# FILE_PATH: open_ticket_ai\src\ce\ticket_system_integration\otobo_adapter_config.py
"""Configuration model for the OTOBO adapter.

This module defines a Pydantic-based configuration model for interacting with an OTOBO server.
It includes settings for server connection, web service operations, and authentication.
The model validates configuration data and securely retrieves sensitive information from environment variables.
"""

import os

from pydantic import BaseModel


class OTOBOAdapterConfig(BaseModel):
    """Configuration model for OTOBO adapter.

    This model defines the necessary configuration parameters to connect and interact with an OTOBO server.
    It includes server details, web service endpoints, and authentication credentials.

    Attributes:
        server_address (str): The base URL of the OTOBO server.
        webservice_name (str): The name of the web service to use.
        search_operation_url (str): The URL for the search operation.
        update_operation_url (str): The URL for the update operation.
        get_operation_url (str): The URL for the get operation.
        username (str): The username for authentication.
        password_env_var (str): The environment variable that contains the password.
    """
    server_address: str
    webservice_name: str
    search_operation_url: str
    update_operation_url: str
    get_operation_url: str
    username: str
    password_env_var: str

    def __str__(self):
        """Return a string representation of the configuration.

        The representation excludes the password for security reasons.

        Returns:
            `str`: A formatted string containing the configuration details (excluding password).
        """
        return f"OTOBOServerConfig(server_address={self.server_address}, " \
               f"webservice_name={self.webservice_name}, " \
               f"search_operation_url={self.search_operation_url}, " \
               f"update_operation_url={self.update_operation_url}, " \
               f"get_operation_url={self.get_operation_url}, " \
               f"username={self.username})"

    @property
    def password(self) -> str:
        """Retrieves the password from the environment variable specified in the configuration.

        Returns:
            `str`: The password for authentication.

        Raises:
            `ValueError`: If the specified environment variable is not set.
        """
        password = os.getenv(self.password_env_var)
        if not password:
            raise ValueError(f"Environment variable '{self.password_env_var}' is not set.")
        return password