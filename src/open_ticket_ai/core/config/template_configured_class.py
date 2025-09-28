from abc import abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from open_ticket_ai.core.config.raw_config import RawConfig

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class TemplateConfiguredClass:
    def __init__(self, config: RawConfig[BaseModel] | BaseModel, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def get_raw_config_model_type() -> type[RawConfig[BaseModel]]:
        pass

    @staticmethod
    def get_rendered_config_model_type() -> type[BaseModel] | None:
        return None

    @staticmethod
    def needs_raw_config() -> bool:
        return True
