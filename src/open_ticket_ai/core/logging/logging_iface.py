from __future__ import annotations

import abc
from typing import Any


class AppLogger(abc.ABC):
    @abc.abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None: ...

    @abc.abstractmethod
    def info(self, message: str, **kwargs: Any) -> None: ...

    @abc.abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None: ...

    @abc.abstractmethod
    def error(self, message: str, **kwargs: Any) -> None: ...

    @abc.abstractmethod
    def exception(self, message: str, **kwargs: Any) -> None: ...


class LoggerFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> AppLogger:
        pass
