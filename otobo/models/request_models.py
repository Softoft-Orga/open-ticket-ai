from dataclasses import dataclass


@dataclass
class AuthData:
    UserLogin: str
    Password: str
