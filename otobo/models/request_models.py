from dataclasses import dataclass


@dataclass
class AuthData:
    """Authentication data used by the OTOBO client."""

    UserLogin: str
    Password: str
