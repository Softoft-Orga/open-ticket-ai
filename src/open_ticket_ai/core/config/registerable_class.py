from typing import Any

from pydantic import BaseModel


class RegisterableClass:
    def __init__(self, config: dict[str, Any] | BaseModel, *args, **kwargs):
        self.__config = config
