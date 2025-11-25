from __future__ import annotations

from pathlib import Path
from sqlite3 import Connection, connect
from typing import Any, ClassVar

from open_ticket_ai import Injectable, InjectableConfig, LoggerFactory, StrictBaseModel


class SqliteStorageParams(StrictBaseModel):
    database: Path | str = Path(":memory:")
    timeout: float = 5.0
    isolation_level: str | None = None


class SqliteStorage(Injectable[SqliteStorageParams]):
    ParamsModel: ClassVar[type[StrictBaseModel]] = SqliteStorageParams

    def __init__(self, config: InjectableConfig, logger_factory: LoggerFactory, *_: Any, **__: Any) -> None:
        super().__init__(config, logger_factory)
        self._connection: Connection | None = None

    def connect(self) -> Connection:
        if self._connection is None:
            database = str(self._params.database)
            self._connection = connect(database, timeout=self._params.timeout, isolation_level=self._params.isolation_level)
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None
